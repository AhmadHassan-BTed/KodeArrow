import sys
import os
import argparse

# Path discovery for enterprise mono-repo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from kode_arrow.config.logging import setup_logging
from kode_arrow.config.settings import Config
from kode_arrow.core.app import KodeArrowApp

def run():
    parser = argparse.ArgumentParser(description="KodeArrow - Professional Productivity Tool")
    parser.add_argument('--version', choices=['standard', 'r_edition'], default='standard',
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
