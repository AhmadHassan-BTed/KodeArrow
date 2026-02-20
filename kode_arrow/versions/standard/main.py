from .app import StandardApp
from ...infrastructure.config.logging_config import setup_logging

def main():
    setup_logging()
    app = StandardApp()
    app.start()

if __name__ == "__main__":
    main()
