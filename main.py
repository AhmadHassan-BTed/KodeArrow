import sys
import os
import argparse

# Path discovery for enterprise mono-repo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from kode_arrow.config.logging import setup_logging
from kode_arrow.config.settings import Config
from kode_arrow.core.app import KodeArrowApp

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
                        print(f"Terminating older active instance with PID {proc.info['pid']}...")
                        proc.terminate()
                        try:
                            proc.wait(timeout=2.0)
                        except psutil.TimeoutExpired:
                            proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Process single-instance check skipped: {e}")

def run():
    kill_other_instances()
    
    parser = argparse.ArgumentParser(description="KodeArrow - Professional Productivity Tool")
    parser.add_argument('--version', choices=['standard', 'r_edition'], default='r_edition',
                        help='Choose the application edition to run')
    args = parser.parse_args()

    setup_logging()
    Config.validate()

    is_research = (args.version == 'r_edition')
    app = KodeArrowApp(is_research=is_research)

    try:
        app.start()
    except KeyboardInterrupt:
        app.stop()

if __name__ == "__main__":
    run()
