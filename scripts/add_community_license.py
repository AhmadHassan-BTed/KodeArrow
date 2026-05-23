import sys
import os

# Put root directory in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import firebase_admin
from firebase_admin import credentials, firestore
from kode_arrow.config.settings import Config

def main():
    print("Initializing Firebase connection using config/.env settings...")
    # Initialize Firebase Admin using credentials from the active config
    cred = credentials.Certificate(Config.FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    email = "freeforever@kodearrow.dev"
    collection = "ControlGroup"
    
    print(f"Checking for document '{email}' in collection '{collection}'...")
    doc_ref = db.collection(collection).document(email)
    doc = doc_ref.get()
    
    data = {
        "email": email,
        "expiration_date": "2099-12-31" # creative lifetime key
    }
    
    if doc.exists:
        print(f"Document '{email}' already exists. Updating/overwriting with lifetime credentials...")
    else:
        print(f"Document '{email}' does not exist. Creating new lifetime document...")
        
    doc_ref.set(data)
    print(f"Successfully configured '{email}' in '{collection}'!")
    
    # Initialize their usage stats in usage/usage_data subcollection!
    usage_ref = doc_ref.collection('usage').document('usage_data')
    if not usage_ref.get().exists:
        print("Initializing usage/usage_data collection for telemetry statistics...")
        usage_ref.set({
            "charactersTyped": 0,
            "kodeArrowHotkeys": 0,
            "TotalUsageMinutes": 0
        })
        print("Telemetry usage subcollection initialized successfully!")
    else:
        print("Telemetry usage subcollection already exists.")

if __name__ == "__main__":
    main()
