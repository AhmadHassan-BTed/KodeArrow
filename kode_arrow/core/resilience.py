"""
KodeArrow Resilience Module
============================
Production-grade defenses against silent process death in windowless (.exe) mode.

Covers:
- NullStream: prevents crashes when sys.stdout/stderr are None (PyInstaller console=False)
- Global exception handlers: catches unhandled exceptions in all threads
- WatchdogThread: monitors keyboard hook health and sends heartbeats
- PowerEventListener: detects Windows sleep/wake and triggers hook recovery
"""

import sys
import os
import time
import ctypes
if sys.platform == "win32":
    import ctypes.wintypes
import threading
import logging

logger = logging.getLogger("KodeArrow.Resilience")



# ---------------------------------------------------------------------------
# 1. NullStream — safe replacement for None stdout/stderr in windowless mode
# ---------------------------------------------------------------------------

class NullStream:
    """A no-op stream that silently absorbs all writes.
    
    PyInstaller with console=False sets sys.stdout and sys.stderr to None.
    Any print() or logging StreamHandler write then raises:
        AttributeError: 'NoneType' object has no attribute 'write'
    
    This class prevents that by acting as a silent sink.
    """

    def write(self, data):
        pass

    def flush(self):
        pass

    def fileno(self):
        return -1

    def isatty(self):
        return False

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return False


def fix_stdio():
    """Replace None stdout/stderr with NullStream to prevent crashes.
    
    MUST be called at the very top of main.py, before any logging or print.
    """
    if sys.stdout is None:
        sys.stdout = NullStream()
    if sys.stderr is None:
        sys.stderr = NullStream()


# ---------------------------------------------------------------------------
# 2. Global Exception Handlers
# ---------------------------------------------------------------------------

def _uncaught_exception_handler(exc_type, exc_value, exc_traceback):
    """Handles uncaught exceptions on the main thread."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow Ctrl+C to work normally
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical(
        "Uncaught exception on MAIN thread",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


def _uncaught_thread_exception_handler(args):
    """Handles uncaught exceptions on ANY background thread (Python 3.8+)."""
    if issubclass(args.exc_type, KeyboardInterrupt):
        return
    logger.critical(
        "Uncaught exception on thread '%s'",
        args.thread.name if args.thread else "<unknown>",
        exc_info=(args.exc_type, args.exc_value, args.exc_traceback)
    )


def install_global_exception_handlers():
    """Install global exception handlers for all threads.
    
    MUST be called early in startup, after logging is configured.
    """
    sys.excepthook = _uncaught_exception_handler
    # threading.excepthook is available in Python 3.8+
    if hasattr(threading, 'excepthook'):
        threading.excepthook = _uncaught_thread_exception_handler
    logger.info("Global exception handlers installed")


# ---------------------------------------------------------------------------
# 3. Watchdog Thread
# ---------------------------------------------------------------------------

class WatchdogThread(threading.Thread):
    """Background thread that monitors application health.
    
    Responsibilities:
    - Sends a heartbeat log every interval (proves the process is alive)
    - Checks if the keyboard hook is still functional
    - Triggers hook re-registration if the hook has died
    - Prevents Windows from classifying the process as idle/suspendable
    """

    def __init__(self, engine, heartbeat_interval=30):
        super().__init__(name="KodeArrow-Watchdog", daemon=True)
        self._engine = engine
        self._interval = heartbeat_interval
        self._stop_event = threading.Event()
        self._recovery_count = 0
        self._power_listener = None

    def stop(self):
        """Signal the watchdog to stop."""
        self._stop_event.set()
        if self._power_listener:
            self._power_listener.stop()

    def run(self):
        logger.info("Watchdog started (heartbeat every %ds)", self._interval)

        # Start the power event listener on a separate thread
        self._power_listener = PowerEventListener(
            on_resume_callback=self._on_power_resume
        )
        self._power_listener.start()

        heartbeat_count = 0
        while not self._stop_event.is_set():
            self._stop_event.wait(timeout=self._interval)
            if self._stop_event.is_set():
                break

            heartbeat_count += 1

            # Heartbeat — proves the process is alive in the log
            logger.debug(
                "Watchdog heartbeat #%d (recoveries: %d)",
                heartbeat_count, self._recovery_count
            )

            # Check hook health
            try:
                if not self._engine.is_hook_alive():
                    logger.warning(
                        "Keyboard hook appears dead — triggering recovery (#%d)",
                        self._recovery_count + 1
                    )
                    self._recover_hooks()
            except Exception:
                logger.exception("Error during watchdog hook health check")

            # Prevent Windows idle classification by resetting the thread's
            # execution timer. This uses SetThreadExecutionState on Windows.
            if sys.platform == "win32":
                try:
                    ES_SYSTEM_REQUIRED = 0x00000001
                    ES_CONTINUOUS = 0x80000000
                    ctypes.windll.kernel32.SetThreadExecutionState(
                        ES_CONTINUOUS | ES_SYSTEM_REQUIRED
                    )
                except Exception:
                    pass  # Non-critical, best-effort

        logger.info("Watchdog stopped")

    def _on_power_resume(self):
        """Called by the PowerEventListener when the system resumes from sleep/hibernate."""
        logger.info("System RESUME detected — scheduling hook recovery in 2s")
        # Small delay to let the OS fully restore all services
        time.sleep(2)
        self._recover_hooks()

    def _recover_hooks(self):
        """Re-register all keyboard hooks."""
        try:
            self._engine.reload_hotkeys()
            self._recovery_count += 1
            logger.info("Hook recovery #%d successful", self._recovery_count)
        except Exception:
            logger.exception("Hook recovery FAILED")


# ---------------------------------------------------------------------------
# 4. Power Event Listener (Win32 & Linux D-Bus)
# ---------------------------------------------------------------------------

class PowerEventListener(threading.Thread):
    """Listens for power events (sleep/wake).
    
    On Windows: uses Win32 RegisterPowerSettingNotification / WM_POWERBROADCAST.
    On Linux: listens to systemd logind PrepareForSleep D-Bus signal.
    """

    # Win32 constants
    WM_POWERBROADCAST = 0x0218
    PBT_APMRESUMEAUTOMATIC = 0x0012
    PBT_APMRESUMESUSPEND = 0x0007
    PBT_APMSUSPEND = 0x0004

    def __init__(self, on_resume_callback):
        super().__init__(name="KodeArrow-PowerListener", daemon=True)
        self._on_resume = on_resume_callback
        self._hwnd = None
        self._stop_event = threading.Event()

    def stop(self):
        """Signal the power listener to stop."""
        self._stop_event.set()
        if sys.platform == "win32" and self._hwnd:
            try:
                user32 = ctypes.windll.user32
                WM_CLOSE = 0x0010
                user32.PostMessageW(self._hwnd, WM_CLOSE, 0, 0)
            except Exception:
                pass

    def run(self):
        if sys.platform == "win32":
            try:
                self._run_win32_message_loop()
            except Exception:
                pass
        elif sys.platform.startswith("linux"):
            try:
                self._run_linux_dbus_listener()
            except Exception:
                pass

    def _run_linux_dbus_listener(self):
        """Listens for systemd PrepareForSleep signal over D-Bus on Linux."""
        import subprocess
        try:
            # Monitor systemd logind PrepareForSleep signals via dbus-monitor
            proc = subprocess.Popen(
                ["dbus-monitor", "--system", "type='signal',interface='org.freedesktop.login1.Manager',member='PrepareForSleep'"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            while not self._stop_event.is_set():
                line = proc.stdout.readline()
                if not line:
                    break
                if "boolean false" in line:  # Resuming from sleep
                    logger.info("Linux D-Bus power event: RESUME detected")
                    threading.Thread(
                        target=self._safe_resume_callback,
                        name="KodeArrow-PowerResume",
                        daemon=True
                    ).start()
        except Exception as e:
            logger.debug("Linux D-Bus power listener inactive: %s", e)

    def _run_win32_message_loop(self):

        """Win32 message loop for power events."""
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        # Define WNDPROC callback type (WPARAM=UINT_PTR, LPARAM=LONG_PTR)
        WNDPROCTYPE = ctypes.WINFUNCTYPE(
            ctypes.c_long,  # LRESULT
            ctypes.c_void_p,  # HWND
            ctypes.c_uint,  # UINT (msg)
            ctypes.c_uint,  # WPARAM
            ctypes.c_long,  # LPARAM
        )

        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == self.WM_POWERBROADCAST:
                if wparam in (self.PBT_APMRESUMEAUTOMATIC, self.PBT_APMRESUMESUSPEND):
                    logger.info("Power event: RESUME detected (wparam=0x%04X)", wparam)
                    threading.Thread(
                        target=self._safe_resume_callback,
                        name="KodeArrow-PowerResume",
                        daemon=True
                    ).start()
                elif wparam == self.PBT_APMSUSPEND:
                    logger.info("Power event: SUSPEND detected")
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        # Keep a reference to prevent garbage collection
        self._wnd_proc = WNDPROCTYPE(wnd_proc)

        # Define WNDCLASSW manually (removed from ctypes.wintypes in Python 3.13)
        class WNDCLASSW(ctypes.Structure):
            _fields_ = [
                ("style", ctypes.c_uint),
                ("lpfnWndProc", ctypes.c_void_p),
                ("cbClsExtra", ctypes.c_int),
                ("cbWndExtra", ctypes.c_int),
                ("hInstance", ctypes.c_void_p),
                ("hIcon", ctypes.c_void_p),
                ("hCursor", ctypes.c_void_p),
                ("hbrBackground", ctypes.c_void_p),
                ("lpszMenuName", ctypes.c_wchar_p),
                ("lpszClassName", ctypes.c_wchar_p),
            ]

        # Register window class
        class_name = "KodeArrowPowerListener"
        wndclass = WNDCLASSW()
        wndclass.style = 0
        wndclass.lpfnWndProc = ctypes.cast(self._wnd_proc, ctypes.c_void_p).value
        wndclass.cbClsExtra = 0
        wndclass.cbWndExtra = 0
        wndclass.hInstance = kernel32.GetModuleHandleW(None)
        wndclass.hIcon = None
        wndclass.hCursor = None
        wndclass.hbrBackground = None
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = class_name

        atom = user32.RegisterClassW(ctypes.byref(wndclass))
        if not atom:
            return

        # Create message-only window (HWND_MESSAGE parent = (HWND)-3)
        self._hwnd = user32.CreateWindowExW(
            0, class_name, "KodeArrow Power Monitor",
            0, 0, 0, 0, 0,
            ctypes.c_void_p(-3), None, kernel32.GetModuleHandleW(None), None
        )

        if not self._hwnd:
            return

        # Message pump
        msg = wintypes.MSG()
        while not self._stop_event.is_set():
            # Use PeekMessage with a timeout approach so we can check stop_event
            result = user32.PeekMessageW(ctypes.byref(msg), self._hwnd, 0, 0, 1)  # PM_REMOVE = 1
            if result:
                if msg.message == 0x0012:  # WM_QUIT
                    break
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
            else:
                # No message — sleep briefly to avoid busy-waiting
                time.sleep(0.5)

        # Cleanup
        if self._hwnd:
            user32.DestroyWindow(self._hwnd)
        user32.UnregisterClassW(class_name, kernel32.GetModuleHandleW(None))
        logger.info("PowerEventListener stopped")

    def _safe_resume_callback(self):
        """Safely invoke the resume callback."""
        try:
            self._on_resume()
        except Exception:
            logger.exception("Error in power resume callback")
