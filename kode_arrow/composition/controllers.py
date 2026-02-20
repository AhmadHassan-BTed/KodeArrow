from __future__ import annotations

import itertools
from typing import Callable, Protocol

from kode_arrow.application.use_cases.navigation_action_use_case import (
    NavigationAction,
    NavigationActionUseCase,
)
from kode_arrow.application.use_cases.telemetry.research_batching_service import (
    ResearchBatchingService,
)


class HotkeyController(Protocol):
    def register(self) -> None:
        ...


class StandardHotkeyController:
    def __init__(
        self,
        *,
        keyboard_port,
        navigation_use_case: NavigationActionUseCase,
    ):
        self._keyboard_port = keyboard_port
        self._navigation_use_case = navigation_use_case

        self._actions = {
            "i": NavigationAction(key_to_press="up", requires_premium=True),
            "j": NavigationAction(key_to_press="left", requires_premium=False),
            "k": NavigationAction(key_to_press="down", requires_premium=True),
            "l": NavigationAction(key_to_press="right", requires_premium=False),
        }

    def register(self) -> None:
        def handle_combo(*k_list: str) -> None:
            for k in k_list:
                self._navigation_use_case.execute(self._actions[k])

        keys = ["i", "j", "k", "l"]
        for r in range(1, 5):
            for combo in itertools.permutations(keys, r):
                hotkey = f"alt+{'+'.join(combo)}"
                # keyboard lib expects 'alt+x+y'
                hotkey = hotkey.replace(" +", "+")
                self._keyboard_port.add_hotkey(
                    hotkey,
                    lambda combo=combo: handle_combo(*combo),
                    suppress=True,
                )

        extended_keys = {
            'u': NavigationAction(key_to_press='home', requires_premium=True),
            'o': NavigationAction(key_to_press='end', requires_premium=True),
            'p': NavigationAction(key_to_press='delete', requires_premium=True),
            ';': NavigationAction(key_to_press='backspace', requires_premium=True),
            '[': NavigationAction(key_to_press='pageup', requires_premium=True),
            "'": NavigationAction(key_to_press='pagedown', requires_premium=True),
        }
        for key, action in extended_keys.items():
            self._keyboard_port.add_hotkey(
                f'alt+{key}',
                lambda a=action: self._navigation_use_case.execute(a),
                suppress=True,
            )


class REditionHotkeyController:
    def __init__(
        self,
        *,
        keyboard_port,
        navigation_use_case: NavigationActionUseCase,
        batching: ResearchBatchingService,
        on_key_event,
    ):
        self._keyboard_port = keyboard_port
        self._navigation_use_case = navigation_use_case
        self._batching = batching
        self._on_key_event = on_key_event

        self._keys = ["i", "j", "k", "l"]

    def register(self) -> None:
        def track_and_execute(k: str) -> None:
            self._batching.record_hotkey()
            if k == "up":
                self._navigation_use_case.execute(
                    NavigationAction(key_to_press="up", requires_premium=True)
                )
            elif k == "down":
                self._navigation_use_case.execute(
                    NavigationAction(key_to_press="down", requires_premium=True)
                )
            elif k == "left":
                self._navigation_use_case.execute(
                    NavigationAction(key_to_press="left", requires_premium=False)
                )
            elif k == "right":
                self._navigation_use_case.execute(
                    NavigationAction(key_to_press="right", requires_premium=False)
                )

        actions = {
            "i": lambda: track_and_execute("up"),
            "j": lambda: track_and_execute("left"),
            "k": lambda: track_and_execute("down"),
            "l": lambda: track_and_execute("right"),
        }

        def handle_combo(*k_list: str) -> None:
            for k in k_list:
                actions[k]()

        for r in range(1, 5):
            for combo in itertools.permutations(self._keys, r):
                hotkey = f"alt+{'+'.join(combo)}"
                hotkey = hotkey.replace(" +", "+")
                self._keyboard_port.add_hotkey(
                    hotkey,
                    lambda combo=combo: handle_combo(*combo),
                    suppress=True,
                )

        # attach character tracking to keyboard events
        self._keyboard_port.on_press(self._on_key_event)

