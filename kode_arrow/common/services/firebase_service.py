import firebase_admin
from firebase_admin import credentials, firestore
from tkinter import messagebox
import logging
from ..config.settings import Config

class FirebaseService:
    """Service class to handle all Firebase/Firestore operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = self._initialize_firestore()

    def _initialize_firestore(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(Config.FIREBASE_CONFIG)
                firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            self.logger.error(f"Failed to initialize Firestore: {e}")
            messagebox.showinfo("Error", "Initialization failed. Please check your internet connection or update to the newest version.")
            return None

    def get_user_doc(self, collection, email):
        if not self.db: return None
        try:
            return self.db.collection(collection).document(email).get()
        except Exception as e:
            self.logger.error(f"Error fetching user document from {collection}: {e}")
            return None

    def update_user_device(self, collection, email, device_id):
        if not self.db: return False
        try:
            user_ref = self.db.collection(collection).document(email)
            devices_ref = user_ref.collection('devices')
            devices_query = devices_ref.get()
            
            device_data = {'id': device_id}
            devices_ref.document(f'device{len(devices_query) + 1}').set(device_data)
            return True
        except Exception as e:
            self.logger.error(f"Error updating user device: {e}")
            return False

    def upload_usage_data(self, collection, email, data):
        """Uploads telemetry/usage data to the specified collection."""
        if not self.db: return False
        try:
            usage_ref = self.db.collection(collection).document(email).collection('usage').document('usage_data')
            doc = usage_ref.get()
            
            if doc.exists:
                existing_data = doc.to_dict()
                for key, value in data.items():
                    existing_data[key] = existing_data.get(key, 0) + value
                usage_ref.set(existing_data)
            else:
                usage_ref.set(data)
            return True
        except Exception as e:
            self.logger.error(f"Error uploading usage data: {e}")
            return False
