import sys
import os
import argparse

# Path discovery for enterprise mono-repo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from kode_arrow.infrastructure.config.logging_config import setup_logging
from kode_arrow.infrastructure.config.settings import Config

def run():
    parser = argparse.ArgumentParser(description="KodeArrow - Professional Productivity Tool")
    parser.add_argument('--version', choices=['standard', 'r_edition'], default='standard',
                        help='Choose the application edition to run')
    args = parser.parse_args()

    setup_logging()
    Config.validate()

    if args.version == 'standard':
        from kode_arrow.versions.standard.app import StandardApp
        app = StandardApp()
    else:
        from kode_arrow.versions.r_edition.app import REditionApp
        app = REditionApp()

    try:
        app.start()
    except KeyboardInterrupt:
        app.stop()

if __name__ == "__main__":
    run()
