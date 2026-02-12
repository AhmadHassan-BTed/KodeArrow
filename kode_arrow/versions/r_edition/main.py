from .app import REditionApp
from ...common.utils.logging_config import setup_logging

def main():
    setup_logging()
    app = REditionApp()
    app.start()

if __name__ == "__main__":
    main()
