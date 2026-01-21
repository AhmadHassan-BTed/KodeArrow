from __future__ import print_function as _print_function

version = '0.13.5'

import re as _re
import itertools as _itertools
import collections as _collections
from threading import Thread as _Thread, Lock as _Lock
import time as _time

_time.monotonic = getattr(_time, 'monotonic', None) or _time.time

try:
    # Python2
    long, basestring
    _is_str = lambda x: isinstance(x, basestring)
    _is_number = lambda x: isinstance(x, (int, long))
    import Queue as _queue
    # threading.Event is a function in Python2 wrappin _Event (?!).
    from threading import _Event as _UninterruptibleEvent
except NameError:
    # Python3
    _is_str = lambda x: isinstance(x, str)
    _is_number = lambda x: isinstance(x, int)
    import queue as _queue
    from threading import Event as _UninterruptibleEvent
_is_list = lambda x: isinstance(x, (list, tuple))

# Just a dynamic object to store attributes for the closures.
class _State(object): pass

# The "Event" class from `threading` ignores signals when waiting and is
# impossible to interrupt with Ctrl+C. So we rewrite `wait` to wait in small,
# interruptible intervals.
class _Event(_UninterruptibleEvent):
    def wait(self):
        while True:
            if _UninterruptibleEvent.wait(self, 0.5):
                break

import platform as _platform
if _platform.system() == 'Windows':
    from. import _winkeyboard as _os_keyboard
elif _platform.system() == 'Linux':
    from. import _nixkeyboard as _os_keyboard
elif _platform.system() == 'Darwin':
    from. import _darwinkeyboard as _os_keyboard
else:
    raise OSError("Unsupported platform '{}'".format(_platform.system()))

from ._keyboard_event import KEY_DOWN, KEY_UP, KeyboardEvent
from ._generic import GenericListener as _GenericListener
from ._canonical_names import all_modifiers, sided_modifiers, normalize_name

_modifier_scan_codes = set()
def is_modifier(key):
    """
    Returns True if `key` is a scan code or name of a modifier key.
    """
    if _is_str(key):
        return key in all_modifiers
    else:
        if not _modifier_scan_codes:
            scan_codes = (key_to_scan_codes(name, False) for name in all_modifiers) 
            _modifier_scan_codes.update(*scan_codes)
        return key in _modifier_scan_codes

_pressed_events_lock = _Lock()
_pressed_events = {}
_physically_pressed_keys = _pressed_events
_logically_pressed_keys = {}
class _KeyboardListener(_GenericListener):
    transition_table = {
        #Current state of the modifier, per `modifier_states`.
        #|
        #|             Type of event that triggered this modifier update.
        #|             |
        #|             |         Type of key that triggered this modiier update.
        #|             |         |
        #|             |         |            Should we send a fake key press?
        #|             |         |            |
        #|             |         |     =>     |       Accept the event?
        #|             |         |            |       |
        #|             |         |            |       |      Next state.
        #v             v         v            v       v      v
        ('free',       KEY_UP,   'modifier'): (False, True,  'free'),
        ('free',       KEY_DOWN, 'modifier'): (False, False, 'pending'),
        ('pending',    KEY_UP,   'modifier'): (True,  True,  'free'),
        ('pending',    KEY_DOWN, 'modifier'): (False, True,  'allowed'),
        ('suppressed', KEY_UP,   'modifier'): (False, False, 'free'),
        ('suppressed', KEY_DOWN, 'modifier'): (False, False, 'suppressed'),
        ('allowed',    KEY_UP,   'modifier'): (False, True,  'free'),
        ('allowed',    KEY_DOWN, 'modifier'): (False, True,  'allowed'),

        ('free',       KEY_UP,   'hotkey'):   (False, None,  'free'),
        ('free',       KEY_DOWN, 'hotkey'):   (False, None,  'free'),
        ('pending',    KEY_UP,   'hotkey'):   (False, None,  'suppressed'),
        ('pending',    KEY_DOWN, 'hotkey'):   (False, None,  'suppressed'),
        ('suppressed', KEY_UP,   'hotkey'):   (False, None,  'suppressed'),
        ('suppressed', KEY_DOWN, 'hotkey'):   (False, None,  'suppressed'),
        ('allowed',    KEY_UP,   'hotkey'):   (False, None,  'allowed'),
        ('allowed',    KEY_DOWN, 'hotkey'):   (False, None,  'allowed'),

        ('free',       KEY_UP,   'other'):    (False, True,  'free'),
        ('free',       KEY_DOWN, 'other'):    (False, True,  'free'),
        ('pending',    KEY_UP,   'other'):    (True,  True,  'allowed'),
        ('pending',    KEY_DOWN, 'other'):    (True,  True,  'allowed'),
        # Necessary when hotkeys are removed after beign triggered, such as
        # TestKeyboard.test_add_hotkey_multistep_suppress_modifier.
        ('suppressed', KEY_UP,   'other'):    (False, False, 'allowed'),
        ('suppressed', KEY_DOWN, 'other'):    (True,  True,  'allowed'),
        ('allowed',    KEY_UP,   'other'):    (False, True,  'allowed'),
        ('allowed',    KEY_DOWN, 'other'):    (False, True,  'allowed'),
    }

    def init(self):
        _os_keyboard.init()

        self.active_modifiers = set()
        self.blocking_hooks = []
        self.blocking_keys = _collections.defaultdict(list)
        self.nonblocking_keys = _collections.defaultdict(list)
        self.blocking_hotkeys = _collections.defaultdict(list)
        self.nonblocking_hotkeys = _collections.defaultdict(list)
        self.filtered_modifiers = _collections.Counter()
        self.is_replaying = False

        # Supporting hotkey suppression is harder than it looks. See
        # https://github.com/boppreh/keyboard/issues/22
        self.modifier_states = {} # "alt" -> "allowed"

    def pre_process_event(self, event):
        for key_hook in self.nonblocking_keys[event.scan_code]:
            key_hook(event)

        with _pressed_events_lock:
            hotkey = tuple(sorted(_pressed_events))
        for callback in self.nonblocking_hotkeys[hotkey]:
            callback(event)

        return event.scan_code or (event.name and event.name != 'unknown')

    def direct_callback(self, event):
        """
        This function is called for every OS keyboard event and decides if the
        event should be blocked or not, and passes a copy of the event to
        other, non-blocking, listeners.

        There are two ways to block events: remapped keys, which translate
        events by suppressing and re-emitting; and blocked hotkeys, which
        suppress specific hotkeys.
        """
        # Pass through all fake key events, don't even report to other handlers.
        if self.is_replaying:
            return True

        if not all(hook(event) for hook in self.blocking_hooks):
            return False

        event_type = event.event_type
        scan_code = event.scan_code

        # Update tables of currently pressed keys and modifiers.
        with _pressed_events_lock:
            if event_type == KEY_DOWN:
                if is_modifier(scan_code): self.active_modifiers.add(scan_code)
                _pressed_events[scan_code] = event
            hotkey = tuple(sorted(_pressed_events))
            if event_type == KEY_UP:
                self.active_modifiers.discard(scan_code)
                if scan_code in _pressed_events: del _pressed_events[scan_code]

        # Mappings based on individual keys instead of hotkeys.
        for key_hook in self.blocking_keys[scan_code]:
            if not key_hook(event):
                return False

        # Default accept.
        accept = True

        if self.blocking_hotkeys:
            if self.filtered_modifiers[scan_code]:
                origin = 'modifier'
                modifiers_to_update = set([scan_code])
            else:
                modifiers_to_update = self.active_modifiers
                if is_modifier(scan_code):
                    modifiers_to_update = modifiers_to_update | {scan_code}
                callback_results = [callback(event) for callback in self.blocking_hotkeys[hotkey]]
                if callback_results:
                    accept = all(callback_results)
                    origin = 'hotkey'
                else:
                    origin = 'other'

            for key in sorted(modifiers_to_update):
                transition_tuple = (self.modifier_states.get(key, 'free'), event_type, origin)
                should_press, new_accept, new_state = self.transition_table[transition_tuple]
                if should_press: press(key)
                if new_accept is not None: accept = new_accept
                self.modifier_states[key] = new_state

        if accept:
            if event_type == KEY_DOWN:
                _logically_pressed_keys[scan_code] = event
            elif event_type == KEY_UP and scan_code in _logically_pressed_keys:
                del _logically_pressed_keys[scan_code]

        # Queue for handlers that won't block the event.
        self.queue.put(event)

        return accept

    def listen(self):
        _os_keyboard.listen(self.direct_callback)

_listener = _KeyboardListener()

def key_to_scan_codes(key, error_if_missing=True):
    """
    Returns a list of scan codes associated with this key (name or scan code).
    """
    if _is_number(key):
        return (key,)
    elif _is_list(key):
        return sum((key_to_scan_codes(i) for i in key), ())
    elif not _is_str(key):
        raise ValueError('Unexpected key type ' + str(type(key)) + ', value (' + repr(key) + ')')

    normalized = normalize_name(key)
    if normalized in sided_modifiers:
        left_scan_codes = key_to_scan_codes('left ' + normalized, False)
        right_scan_codes = key_to_scan_codes('right ' + normalized, False)
        return left_scan_codes + tuple(c for c in right_scan_codes if c not in left_scan_codes)

    try:
        # Put items in ordered dict to remove duplicates.
        t = tuple(_collections.OrderedDict((scan_code, True) for scan_code, modifier in _os_keyboard.map_name(normalized)))
        e = None
    except (KeyError, ValueError) as exception:
        t = ()
        e = exception

    if not t and error_if_missing:
        raise ValueError('Key {} is not mapped to any known key.'.format(repr(key)), e)
    else:
        return t

def parse_hotkey(hotkey):
    """
    Parses a user-provided hotkey into nested tuples representing the
    parsed structure, with the bottom values being lists of scan codes.
    Also accepts raw scan codes, which are then wrapped in the required
    number of nestings.

    Example:

        parse_hotkey("alt+shift+a, alt+b, c")
        #    Keys:    ^~^ ^~~~^ ^  ^~^ ^  ^
        #    Steps:   ^~~~~~~~~~^  ^~~~^  ^

        # ((alt_codes, shift_codes, a_codes), (alt_codes, b_codes), (c_codes,))
    """
    if _is_number(hotkey) or len(hotkey) == 1:
        scan_codes = key_to_scan_codes(hotkey)
        step = (scan_codes,)
        steps = (step,)
        return steps
    elif _is_list(hotkey):
        if not any(map(_is_list, hotkey)):
            step = tuple(key_to_scan_codes(k) for k in hotkey)
            steps = (step,)
            return steps
        return hotkey

    steps = []
    for step in _re.split(r',\s?', hotkey):
        keys = _re.split(r'\s?\+\s?', step)
        steps.append(tuple(key_to_scan_codes(key) for key in keys))
    return tuple(steps)

def send(hotkey, do_press=True, do_release=True):
    """
    Sends OS events that perform the given *hotkey* hotkey.

    - `hotkey` can be either a scan code (e.g. 57 for space), single key
    (e.g. 'space') or multi-key, multi-step hotkey (e.g. 'alt+F4, enter').
    - `do_press` if true then press events are sent. Defaults to True.
    - `do_release` if true then release events are sent. Defaults to True.

        send(57)
        send('ctrl+alt+del')
        send('alt+F4, enter')
        send('shift+s')

    Note: keys are released in the opposite order they were pressed.
    """
    _listener.is_replaying = True

    parsed = parse_hotkey(hotkey)
    for step in parsed:
        if do_press:
            for scan_codes in step:
                _os_keyboard.press(scan_codes[0])

        if do_release:
            for scan_codes in reversed(step):
                _os_keyboard.release(scan_codes[0])

    _listener.is_replaying = False

# Alias.
press_and_release = send

def press(hotkey):
    """ Presses and holds down a hotkey (see `send`). """
    send(hotkey, True, False)

def release(hotkey):
    """ Releases a hotkey (see `send`). """
    send(hotkey, False, True)

def is_pressed(hotkey):
    """
    Returns True if the key is pressed.

        is_pressed(57) #-> True
        is_pressed('space') #-> True
        is_pressed('ctrl+space') #-> True
    """
    _listener.start_if_necessary()

    if _is_number(hotkey):
        # Shortcut.
        with _pressed_events_lock:
            return hotkey in _pressed_events

    steps = parse_hotkey(hotkey)
    if len(steps) > 1:
        raise ValueError("Impossible to check if multi-step hotkeys are pressed (`a+b` is ok, `a, b` isn't).")

    # Convert _pressed_events into a set 
    with _pressed_events_lock:
        pressed_scan_codes = set(_pressed_events)
    for scan_codes in steps[0]:
        if not any(scan_code in pressed_scan_codes for scan_code in scan_codes):
            return False
    return True

def call_later(fn, args=(), delay=0.001):
    """
    Calls the provided function in a new thread after waiting some time.
    Useful for giving the system some time to process an event, without blocking
    the current execution flow.
    """
    thread = _Thread(target=lambda: (_time.sleep(delay), fn(*args)))
    thread.start()

_hooks = {}
def hook(callback, suppress=False, on_remove=lambda: None):
    """
    Installs a global listener on all available keyboards, invoking `callback`
    each time a key is pressed or released.
    
    The event passed to the callback is of type `keyboard.KeyboardEvent`,
    with the following attributes:

    - `name`: an Unicode representation of the character (e.g. "&") or
    description (e.g.  "space"). The name is always lower-case.
    - `scan_code`: number representing the physical key, e.g. 55.
    - `time`: timestamp of the time the event occurred, with as much precision
    as given by the OS.

    Returns the given callback for easier development.
    """
    if suppress:
        _listener.start_if_necessary()
        append, remove = _listener.blocking_hooks.append, _listener.blocking_hooks.remove
    else:
        append, remove = _listener.add_handler, _listener.remove_handler

    append(callback)
    def remove_():
        del _hooks[callback]
        del _hooks[remove_]
        remove(callback)
        on_remove()
    _hooks[callback] = _hooks[remove_] = remove_
    return remove_

def on_press(callback, suppress=False):
    """
    Invokes `callback` for every KEY_DOWN event. For details see `hook`.
    """
    return hook(lambda e: e.event_type == KEY_UP or callback(e), suppress=suppress)

def on_release(callback, suppress=False):
    """
    Invokes `callback` for every KEY_UP event. For details see `hook`.
    """
    return hook(lambda e: e.event_type == KEY_DOWN or callback(e), suppress=suppress)

def hook_key(key, callback, suppress=False):
    """
    Hooks key up and key down events for a single key. Returns the event handler
    created. To remove a hooked key use `unhook_key(key)` or
    `unhook_key(handler)`.

    Note: this function shares state with hotkeys, so `clear_all_hotkeys`
    affects it as well.
    """
    _listener.start_if_necessary()
    store = _listener.blocking_keys if suppress else _listener.nonblocking_keys
    scan_codes = key_to_scan_codes(key)
    for scan_code in scan_codes:
        store[scan_code].append(callback)

    def remove_():
        del _hooks[callback]
        del _hooks[key]
        del _hooks[remove_]
        for scan_code in scan_codes:
            store[scan_code].remove(callback)
    _hooks[callback] = _hooks[key] = _hooks[remove_] = remove_
    return remove_

def on_press_key(key, callback, suppress=False):
    """
    Invokes `callback` for KEY_DOWN event related to the given key. For details see `hook`.
    """
    return hook_key(key, lambda e: e.event_type == KEY_UP or callback(e), suppress=suppress)

def on_release_key(key, callback, suppress=False):
    """
    Invokes `callback` for KEY_UP event related to the given key. For details see `hook`.
    """
    return hook_key(key, lambda e: e.event_type == KEY_DOWN or callback(e), suppress=suppress)

def unhook(remove):
    """
    Removes a previously added hook, either by callback or by the return value
    of `hook`.
    """
    _hooks[remove]()
unhook_key = unhook

def unhook_all():
    """
    Removes all keyboard hooks in use, including hotkeys, abbreviations, word
    listeners, `record`ers and `wait`s.
    """
    _listener.start_if_necessary()
    _listener.blocking_keys.clear()
    _listener.nonblocking_keys.clear()
    del _listener.blocking_hooks[:]
    del _listener.handlers[:]
    unhook_all_hotkeys()

def block_key(key):
    """
    Suppresses all key events of the given key, regardless of modifiers.
    """
    return hook_key(key, lambda e: False, suppress=True)
unblock_key = unhook_key

def remap_key(src, dst):
    """
    Whenever the key `src` is pressed or released, regardless of modifiers,
    press or release the hotkey `dst` instead.
    """
    def handler(event):
        if event.event_type == KEY_DOWN:
            press(dst)
        else:
            release(dst)
        return False
    return hook_key(src, handler, suppress=True)
unremap_key = unhook_key

def parse_hotkey_combinations(hotkey):
    """
    Parses a user-provided hotkey. Differently from `parse_hotkey`,
    instead of each step being a list of the different scan codes for each key,
    each step is a list of all possible combinations of those scan codes.
    """
    def combine_step(step):
        # A single step may be composed of many keys, and each key can have
        # multiple scan codes. To speed up hotkey matching and avoid introducing
        # event delays, we list all possible combinations of scan codes for these
        # keys. Hotkeys are usually small, and there are not many combinations, so
        # this is not as insane as it sounds.
        return (tuple(sorted(scan_codes)) for scan_codes in _itertools.product(*step))

    return tuple(tuple(combine_step(step)) for step in parse_hotkey(hotkey))

def _add_hotkey_step(handler, combinations, suppress):
    """
    Hooks a single-step hotkey (e.g. 'shift+a').
    """
    container = _listener.blocking_hotkeys if suppress else _listener.nonblocking_hotkeys

    # Register the scan codes of every possible combination of
    # modfiier + main key. Modifiers have to be registered in 
    # filtered_modifiers too, so suppression and replaying can work.
    for scan_codes in combinations:
        for scan_code in scan_codes:
            if is_modifier(scan_code):
                _listener.filtered_modifiers[scan_code] += 1
        container[scan_codes].append(handler)

    def remove():
        for scan_codes in combinations:
            for scan_code in scan_codes:
                if is_modifier(scan_code):
                    _listener.filtered_modifiers[scan_code] -= 1
            container[scan_codes].remove(handler)
    return remove

_hotkeys = {}
def add_hotkey(hotkey, callback, args=(), suppress=False, timeout=1, trigger_on_release=False):
    """
    Invokes a callback every time a hotkey is pressed. The hotkey must
    be in the format `ctrl+shift+a, s`. This would trigger when the user holds
    ctrl, shift and "a" at once, releases, and then presses "s". To represent
    literal commas, pluses, and spaces, use their names ('comma', 'plus',
    'space').

    - `args` is an optional list of arguments to passed to the callback during
    each invocation.
    - `suppress` defines if successful triggers should block the keys from being
    sent to other programs.
    - `timeout` is the amount of seconds allowed to pass between key presses.
    - `trigger_on_release` if true, the callback is invoked on key release instead
    of key press.

    The event handler function is returned. To remove a hotkey call
    `remove_hotkey(hotkey)` or `remove_hotkey(handler)`.
    before the hotkey state is reset.

    Note: hotkeys are activated when the last key is *pressed*, not released.
    Note: the callback is executed in a separate thread, asynchronously. For an
    example of how to use a callback synchronously, see `wait`.

    Examples:

        # Different but equivalent ways to listen for a spacebar key press.
        add_hotkey(' ', print, args=['space was pressed'])
        add_hotkey('space', print, args=['space was pressed'])
        add_hotkey('Space', print, args=['space was pressed'])
        # Here 57 represents the keyboard code for spacebar; so you will be
        # pressing 'spacebar', not '57' to activate the print function.
        add_hotkey(57, print, args=['space was pressed'])

        add_hotkey('ctrl+q', quit)
        add_hotkey('ctrl+alt+enter, space', some_callback)
    """
    if args:
        callback = lambda callback=callback: callback(*args)

    _listener.start_if_necessary()

    steps = parse_hotkey_combinations(hotkey)

    event_type = KEY_UP if trigger_on_release else KEY_DOWN
    if len(steps) == 1:
        # Deciding when to allow a KEY_UP event is far harder than I thought,
        # and any mistake will make that key "sticky". Therefore just let all
        # KEY_UP events go through as long as that's not what we are listening
        # for.
        handler = lambda e: (event_type == KEY_DOWN and e.event_type == KEY_UP and e.scan_code in _logically_pressed_keys) or (event_type == e.event_type and callback())
        remove_step = _add_hotkey_step(handler, steps[0], suppress)
        def remove_():
            remove_step()
            del _hotkeys[hotkey]
            del _hotkeys[remove_]
            del _hotkeys[callback]
        # TODO: allow multiple callbacks for each hotkey without overwriting the
        # remover.
        _hotkeys[hotkey] = _hotkeys[remove_] = _hotkeys[callback] = remove_
        return remove_

    state = _State()
    state.remove_catch_misses = None
    state.remove_last_step = None
    state.suppressed_events = []
    state.last_update = float('-inf')
    
    def catch_misses(event, force_fail=False):
        if (
                event.event_type == event_type
                and state.index
                and event.scan_code not in allowed_keys_by_step[state.index]
            ) or (
                timeout
                and _time.monotonic() - state.last_update >= timeout
            ) or force_fail: # Weird formatting to ensure short-circuit.

            state.remove_last_step()

            for event in state.suppressed_events:
                if event.event_type == KEY_DOWN:
                    press(event.scan_code)
                else:
                    release(event.scan_code)
            del state.suppressed_events[:]

            index = 0
            set_index(0)
        return True

    def set_index(new_index):
        state.index = new_index

        if new_index == 0:
            # This is done for performance reasons, avoiding a global key hook
            # that is always on.
            state.remove_catch_misses = lambda: None
        elif new_index == 1:
            state.remove_catch_misses()
            # Must be `suppress=True` to ensure `send` has priority.
            state.remove_catch_misses = hook(catch_misses, suppress=True)

        if new_index == len(steps) - 1:
            def handler(event):
                if event.event_type == KEY_UP:
                    remove()
                    set_index(0)
                accept = event.event_type == event_type and callback() 
                if accept:
                    return catch_misses(event, force_fail=True)
                else:
                    state.suppressed_events[:] = [event]
                    return False
            remove = _add_hotkey_step(handler, steps[state.index], suppress)
        else:
            # Fix value of next_index.
            def handler(event, new_index=state.index+1):
                if event.event_type == KEY_UP:
                    remove()
                    set_index(new_index)
                state.suppressed_events.append(event)
                return False
            remove = _add_hotkey_step(handler, steps[state.index], suppress)
        state.remove_last_step = remove
        state.last_update = _time.monotonic()
        return False
    set_index(0)

    allowed_keys_by_step = [
        set().union(*step)
        for step in steps
    ]

    def remove_():
        state.remove_catch_misses()
        state.remove_last_step()
        del _hotkeys[hotkey]
        del _hotkeys[remove_]
        del _hotkeys[callback]
    # TODO: allow multiple callbacks for each hotkey without overwriting the
    # remover.
    _hotkeys[hotkey] = _hotkeys[remove_] = _hotkeys[callback] = remove_
    return remove_
register_hotkey = add_hotkey

def remove_hotkey(hotkey_or_callback):
    """
    Removes a previously hooked hotkey. Must be called with the value returned
    by `add_hotkey`.
    """
    _hotkeys[hotkey_or_callback]()
unregister_hotkey = clear_hotkey = remove_hotkey

def unhook_all_hotkeys():
    """
    Removes all keyboard hotkeys in use, including abbreviations, word listeners,
    `record`ers and `wait`s.
    """
    # Because of "alises" some hooks may have more than one entry, all of which
    # are removed together.
    _listener.blocking_hotkeys.clear()
    _listener.nonblocking_hotkeys.clear()
unregister_all_hotkeys = remove_all_hotkeys = clear_all_hotkeys = unhook_all_hotkeys

def remap_hotkey(src, dst, suppress=True, trigger_on_release=False):
    """
    Whenever the hotkey `src` is pressed, suppress it and send
    `dst` instead.

    Example:

        remap('alt+w', 'ctrl+up')
    """
    def handler():
        active_modifiers = sorted(modifier for modifier, state in _listener.modifier_states.items() if state == 'allowed')
        for modifier in active_modifiers:
            release(modifier)
        send(dst)
        for modifier in reversed(active_modifiers):
            press(modifier)
        return False
    return add_hotkey(src, handler, suppress=suppress, trigger_on_release=trigger_on_release)
unremap_hotkey = remove_hotkey

def stash_state():
    """
    Builds a list of all currently pressed scan codes, releases them and returns
    the list. Pairs well with `restore_state` and `restore_modifiers`.
    """
    # TODO: stash caps lock / numlock /scrollock state.
    with _pressed_events_lock:
        state = sorted(_pressed_events)
    for scan_code in state:
        _os_keyboard.release(scan_code)
    return state

def restore_state(scan_codes):
    """
    Given a list of scan_codes ensures these keys, and only these keys, are
    pressed. Pairs well with `stash_state`, alternative to `restore_modifiers`.
    """
    _listener.is_replaying = True

    with _pressed_events_lock:
        current = set(_pressed_events)
    target = set(scan_codes)
    for scan_code in current - target:
        _os_keyboard.release(scan_code)
    for scan_code in target - current:
        _os_keyboard.press(scan_code)

    _listener.is_replaying = False

def restore_modifiers(scan_codes):
    """
    Like `restore_state`, but only restores modifier keys.
    """
    restore_state((scan_code for scan_code in scan_codes if is_modifier(scan_code)))

def write(text, delay=0, restore_state_after=True, exact=None):
    """
    Sends artificial keyboard events to the OS, simulating the typing of a given
    text. Characters not available on the keyboard are typed as explicit unicode
    characters using OS-specific functionality, such as alt+codepoint.

    To ensure text integrity, all currently pressed keys are released before
    the text is typed, and modifiers are restored afterwards.

    - `delay` is the number of seconds to wait between keypresses, defaults to
    no delay.
    - `restore_state_after` can be used to restore the state of pressed keys
    after the text is typed, i.e. presses the keys that were released at the
    beginning. Defaults to True.
    - `exact` forces typing all characters as explicit unicode (e.g.
    alt+codepoint or special events). If None, uses platform-specific suggested
    value.
    """
    if exact is None:
        exact = _platform.system() == 'Windows'

    state = stash_state()
    
    # Window's typing of unicode characters is quite efficient and should be preferred.
    if exact:
        for letter in text:
            if letter in '\n\b':
                send(letter)
            else:
                _os_keyboard.type_unicode(letter)
            if delay: _time.sleep(delay)
    else:
        for letter in text:
            try:
                entries = _os_keyboard.map_name(normalize_name(letter))
                scan_code, modifiers = next(iter(entries))
            except (KeyError, ValueError):
                _os_keyboard.type_unicode(letter)
                continue
            
            for modifier in modifiers:
                press(modifier)

            _os_keyboard.press(scan_code)
            _os_keyboard.release(scan_code)

            for modifier in modifiers:
                release(modifier)

            if delay:
                _time.sleep(delay)

    if restore_state_after:
        restore_modifiers(state)

def wait(hotkey=None, suppress=False, trigger_on_release=False):
    """
    Blocks the program execution until the given hotkey is pressed or,
    if given no parameters, blocks forever.
    """
    if hotkey:
        lock = _Event()
        remove = add_hotkey(hotkey, lambda: lock.set(), suppress=suppress, trigger_on_release=trigger_on_release)
        lock.wait()
        remove_hotkey(remove)
    else:
        while True:
            _time.sleep(1e6)

def get_hotkey_name(names=None):
    """
    Returns a string representation of hotkey from the given key names, or
    the currently pressed keys if not given.  This function:

    - normalizes names;
    - removes "left" and "right" prefixes;
    - replaces the "+" key name with "plus" to avoid ambiguity;
    - puts modifier keys first, in a standardized order;
    - sort remaining keys;
    - finally, joins everything with "+".

    Example:

        get_hotkey_name(['+', 'left ctrl', 'shift'])
        # "ctrl+shift+plus"
    """
    if names is None:
        _listener.start_if_necessary()
        with _pressed_events_lock:
            names = [e.name for e in _pressed_events.values()]
    else:
        names = [normalize_name(name) for name in names]
    clean_names = set(e.replace('left ', '').replace('right ', '').replace('+', 'plus') for e in names)
    # https://developer.apple.com/macos/human-interface-guidelines/input-and-output/keyboard/
    # > List modifier keys in the correct order. If you use more than one modifier key in a
    # > hotkey, always list them in this order: Control, Option, Shift, Command.
    modifiers = ['ctrl', 'alt', 'shift', 'windows']
    sorting_key = lambda k: (modifiers.index(k) if k in modifiers else 5, str(k))
    return '+'.join(sorted(clean_names, key=sorting_key))

def read_event(suppress=False):
    """
    Blocks until a keyboard event happens, then returns that event.
    """
    queue = _queue.Queue(maxsize=1)
    hooked = hook(queue.put, suppress=suppress)
    while True:
        event = queue.get()
        unhook(hooked)
        return event

def read_key(suppress=False):
    """
    Blocks until a keyboard event happens, then returns that event's name or,
    if missing, its scan code.
    """
    event = read_event(suppress)
    return event.name or event.scan_code

def read_hotkey(suppress=True):
    """
    Similar to `read_key()`, but blocks until the user presses and releases a
    hotkey (or single key), then returns a string representing the hotkey
    pressed.

    Example:

        read_hotkey()
        # "ctrl+shift+p"
    """
    queue = _queue.Queue()
    fn = lambda e: queue.put(e) or e.event_type == KEY_DOWN
    hooked = hook(fn, suppress=suppress)
    while True:
        event = queue.get()
        if event.event_type == KEY_UP:
            unhook(hooked)
            with _pressed_events_lock:
                names = [e.name for e in _pressed_events.values()] + [event.name]
            return get_hotkey_name(names)

def get_typed_strings(events, allow_backspace=True):
    """
    Given a sequence of events, tries to deduce what strings were typed.
    Strings are separated when a non-textual key is pressed (such as tab or
    enter). Characters are converted to uppercase according to shift and
    capslock status. If `allow_backspace` is True, backspaces remove the last
    character typed.

    This function is a generator, so you can pass an infinite stream of events
    and convert them to strings in real time.

    Note this functions is merely an heuristic. Windows for example keeps per-
    process keyboard state such as keyboard layout, and this information is not
    available for our hooks.

        get_type_strings(record()) #-> ['This is what', 'I recorded', '']
    """
    backspace_name = 'delete' if _platform.system() == 'Darwin' else 'backspace'

    shift_pressed = False
    capslock_pressed = False
    string = ''
    for event in events:
        name = event.name

        # Space is the only key that we _parse_hotkey to the spelled out name
        # because of legibility. Now we have to undo that.
        if event.name == 'space':
            name = ' '

        if 'shift' in event.name:
            shift_pressed = event.event_type == 'down'
        elif event.name == 'caps lock' and event.event_type == 'down':
            capslock_pressed = not capslock_pressed
        elif allow_backspace and event.name == backspace_name and event.event_type == 'down':
            string = string[:-1]
        elif event.event_type == 'down':
            if len(name) == 1:
                if shift_pressed ^ capslock_pressed:
                    name = name.upper()
                string = string + name
            else:
                yield string
                string = ''
    yield string

_recording = None
def start_recording(recorded_events_queue=None):
    """
    Starts recording all keyboard events into a global variable, or the given
    queue if any. Returns the queue of events and the hooked function.

    Use `stop_recording()` or `unhook(hooked_function)` to stop.
    """
    recorded_events_queue = recorded_events_queue or _queue.Queue()
    global _recording
    _recording = (recorded_events_queue, hook(recorded_events_queue.put))
    return _recording

def stop_recording():
    """
    Stops the global recording of events and returns a list of the events
    captured.
    """
    global _recording
    if not _recording:
        raise ValueError('Must call "start_recording" before.')
    recorded_events_queue, hooked = _recording
    unhook(hooked)
    return list(recorded_events_queue.queue)

def record(until='escape', suppress=False, trigger_on_release=False):
    """
    Records all keyboard events from all keyboards until the user presses the
    given hotkey. Then returns the list of events recorded, of type
    `keyboard.KeyboardEvent`. Pairs well with
    `play(events)`.

    Note: this is a blocking function.
    Note: for more details on the keyboard hook and events see `hook`.
    """
    start_recording()
    wait(until, suppress=suppress, trigger_on_release=trigger_on_release)
    return stop_recording()

def play(events, speed_factor=1.0):
    """
    Plays a sequence of recorded events, maintaining the relative time
    intervals. If speed_factor is <= 0 then the actions are replayed as fast
    as the OS allows. Pairs well with `record()`.

    Note: the current keyboard state is cleared at the beginning and restored at
    the end of the function.
    """
    state = stash_state()

    last_time = None
    for event in events:
        if speed_factor > 0 and last_time is not None:
            _time.sleep((event.time - last_time) / speed_factor)
        last_time = event.time

        key = event.scan_code or event.name
        press(key) if event.event_type == KEY_DOWN else release(key)

    restore_modifiers(state)
replay = play

_word_listeners = {}
def add_word_listener(word, callback, triggers=['space'], match_suffix=False, timeout=2):
    """
    Invokes a callback every time a sequence of characters is typed (e.g. 'pet')
    and followed by a trigger key (e.g. space). Modifiers (e.g. alt, ctrl,
    shift) are ignored.

    - `word` the typed text to be matched. E.g. 'pet'.
    - `callback` is an argument-less function to be invoked each time the word
    is typed.
    - `triggers` is the list of keys that will cause a match to be checked. If
    the user presses some key that is not a character (len>1) and not in
    triggers, the characters so far will be discarded. By default the trigger
    is only `space`.
    - `match_suffix` defines if endings of words should also be checked instead
    of only whole words. E.g. if true, typing 'carpet'+space will trigger the
    listener for 'pet'. Defaults to false, only whole words are checked.
    - `timeout` is the maximum number of seconds between typed characters before
    the current word is discarded. Defaults to 2 seconds.

    Returns the event handler created. To remove a word listener use
    `remove_word_listener(word)` or `remove_word_listener(handler)`.

    Note: all actions are performed on key down. Key up events are ignored.
    Note: word matches are **case sensitive**.
    """
    state = _State()
    state.current = ''
    state.time = -1

    def handler(event):
        name = event.name
        if event.event_type == KEY_UP or name in all_modifiers: return

        if timeout and event.time - state.time > timeout:
            state.current = ''
        state.time = event.time

        matched = state.current == word or (match_suffix and state.current.endswith(word))
        if name in triggers and matched:
            callback()
            state.current = ''
        elif len(name) > 1:
            state.current = ''
        else:
            state.current += name

    hooked = hook(handler)
    def remove():
        hooked()
        del _word_listeners[word]
        del _word_listeners[handler]
        del _word_listeners[remove]
    _word_listeners[word] = _word_listeners[handler] = _word_listeners[remove] = remove
    # TODO: allow multiple word listeners and removing them correctly.
    return remove

def remove_word_listener(word_or_handler):
    """
    Removes a previously registered word listener. Accepts either the word used
    during registration (exact string) or the event handler returned by the
    `add_word_listener` or `add_abbreviation` functions.
    """
    _word_listeners[word_or_handler]()

def add_abbreviation(source_text, replacement_text, match_suffix=False, timeout=2):
    """
    Registers a hotkey that replaces one typed text with another. For example

        add_abbreviation('tm', u'™')

    Replaces every "tm" followed by a space with a ™ symbol (and no space). The
    replacement is done by sending backspace events.

    - `match_suffix` defines if endings of words should also be checked instead
    of only whole words. E.g. if true, typing 'carpet'+space will trigger the
    listener for 'pet'. Defaults to false, only whole words are checked.
    - `timeout` is the maximum number of seconds between typed characters before
    the current word is discarded. Defaults to 2 seconds.
    
    For more details see `add_word_listener`.
    """
    replacement = '\b'*(len(source_text)+1) + replacement_text
    callback = lambda: write(replacement)
    return add_word_listener(source_text, callback, match_suffix=match_suffix, timeout=timeout)

# Aliases.
register_word_listener = add_word_listener
register_abbreviation = add_abbreviation
remove_abbreviation = remove_word_listener