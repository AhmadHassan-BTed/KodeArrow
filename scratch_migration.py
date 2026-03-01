import os
import sys
from dateutil.relativedelta import relativedelta
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kode_arrow.services.firebase import FirebaseService
from kode_arrow.config.settings import Config

Config.validate()
firebase_service = FirebaseService()
db = firebase_service.db

def run_migration():
    for collection_name in ['users', 'ControlGroup']:
        print(f"--- Migrating collection: {collection_name} ---")
        docs = db.collection(collection_name).stream()
        for doc in docs:
            data = doc.to_dict()
            email = doc.id
            sub_date_str = data.get('subscription_date')
            
            updates = {}
            updates['email'] = email
            
            if sub_date_str:
                try:
                    sub_date = datetime.strptime(sub_date_str, '%Y-%m-%d')
                    exp_date = sub_date + relativedelta(months=1)
                    updates['expiration_date'] = exp_date.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"   -> [ERROR] Failed to parse date for {email}: {e}")
            else:
                # Fallback if no sub_date exists
                updates['expiration_date'] = (datetime.today() + relativedelta(months=1)).strftime('%Y-%m-%d')
            
            print(f"Updating {email} -> {updates}")
            db.collection(collection_name).document(email).update(updates)
            
    print("Migration complete!")

if __name__ == '__main__':
    run_migration()
