from .app import REditionApp
from ...infrastructure.config.logging_config import setup_logging

def main():
    setup_logging()
    app = REditionApp()
    app.start()

if __name__ == "__main__":
    main()
