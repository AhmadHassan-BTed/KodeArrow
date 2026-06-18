import sys
import os

# =============================================================================
# CRITICAL: Fix stdio BEFORE any imports that might print or log.
# In windowless mode (PyInstaller console=False), sys.stdout and sys.stderr
# are None. Any print/log to them would crash the process silently.
# =============================================================================
from kode_arrow.core.resilience import fix_stdio
fix_stdio()

import argparse
import logging
import time
import traceback

# Path discovery for enterprise mono-repo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from kode_arrow.config.logging import setup_logging
from kode_arrow.config.settings import Config
from kode_arrow.core.app import KodeArrowApp
from kode_arrow.core.resilience import install_global_exception_handlers

logger = logging.getLogger("KodeArrow.Main")

# Maximum number of in-process restart attempts before giving up
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 3


def kill_other_instances():
    """Finds and terminates any other active older instances of KodeArrow."""
    try:
        import psutil
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['pid'] != current_pid:
                    is_match = False
                    if getattr(sys, 'frozen', False):
                        # Running as compiled binary
                        if proc.info['name'].lower() == "kodearrow.exe":
                            is_match = True
                    else:
                        # Running as python script in dev
                        if "python" in proc.info['name'].lower():
                            cmdline = proc.info.get('cmdline') or []
                            if any("main.py" in arg for arg in cmdline):
                                is_match = True
                                
                    if is_match:
                        logger.info(f"Terminating older active instance with PID {proc.info['pid']}...")
                        proc.terminate()
                        try:
                            proc.wait(timeout=2.0)
                        except psutil.TimeoutExpired:
                            proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        logger.warning(f"Process single-instance check skipped: {e}")

def run():
    kill_other_instances()
    
    parser = argparse.ArgumentParser(description="KodeArrow - Professional Productivity Tool")
    parser.add_argument('--version', choices=['standard', 'r_edition'], default='r_edition',
                        help='Choose the application edition to run')
    args = parser.parse_args()

    setup_logging()
    install_global_exception_handlers()
    Config.validate()

    is_research = (args.version == 'r_edition')
    
    # =========================================================================
    # Retry loop: if the app crashes, restart it in-process up to MAX_RETRIES
    # times. This handles transient failures like pystray crashes after
    # sleep/wake, or unexpected hook failures.
    # =========================================================================
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if attempt > 1:
                logger.warning(
                    "=== RESTART ATTEMPT %d/%d (after %ds cooldown) ===",
                    attempt, MAX_RETRIES, RETRY_DELAY_SECONDS
                )
            
            app = KodeArrowApp(is_research=is_research)
            app.start()
            
            # If start() returns cleanly (user chose Exit), break out
            break
            
        except KeyboardInterrupt:
            logger.info("Received KeyboardInterrupt — shutting down")
            try:
                app.stop()
            except Exception:
                pass
            break
            
        except SystemExit:
            # Allow explicit sys.exit() / os._exit() to work
            break
            
        except Exception:
            logger.critical(
                "KodeArrow crashed on attempt %d/%d",
                attempt, MAX_RETRIES,
                exc_info=True
            )
            
            if attempt < MAX_RETRIES:
                logger.info("Waiting %ds before restart...", RETRY_DELAY_SECONDS)
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.critical(
                    "All %d restart attempts exhausted. "
                    "Launching a fresh process as last resort...",
                    MAX_RETRIES
                )
                _restart_as_new_process()


def _restart_as_new_process():
    """Last-resort: spawn a brand new process of ourselves and exit."""
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled .exe
            executable = sys.executable
            os.execv(executable, [executable] + sys.argv[1:])
        else:
            # Running as python script
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        logger.critical("Failed to restart as new process", exc_info=True)


if __name__ == "__main__":
    run()
