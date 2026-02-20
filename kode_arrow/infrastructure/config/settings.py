import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration management."""
    APP_NAME = os.getenv("APP_NAME", "KodeArrow")
    APP_VERSION = os.getenv("APP_VERSION", "2.5.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Firebase Configuration
    FIREBASE_CONFIG = {
        "type": os.getenv("FIREBASE_TYPE", "service_account"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}",
        "universe_domain": "googleapis.com"
    }

    # Security
    LICENSE_KEY_STANDARD = os.getenv("LICENSE_KEY_STANDARD", "BTED-KAKS-P2SE-2023")

    @classmethod
    def validate(cls):
        """Ensure critical configuration is present."""
        critical_keys = ["FIREBASE_PROJECT_ID", "FIREBASE_PRIVATE_KEY", "FIREBASE_CLIENT_EMAIL"]
        missing = [key for key in critical_keys if not os.getenv(key)]
        if missing:
            print(f"Warning: Missing critical configuration: {', '.join(missing)}")
            return False
        return True
