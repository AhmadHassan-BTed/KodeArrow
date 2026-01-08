import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('kodearrow-server-firebase-adminsdk-9qxya-d2f88510eb.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def add_email_as_admin(email):

    # Add the email to Firestore users collection
    doc_ref_user = db.collection('users').document(email)
    doc_user = doc_ref_user.get()
    if doc_user.exists:
        print(f"Email '{email}' already exists in Firestore users collection.")
    else:
        # Add the email to Firestore users collection
        doc_ref_user.set({'email': email})
        print(f"Added '{email}' to users collection.")

    # Prompt user to enter up to 4 device IDs
    devices = []
    for i in range(4):
        device_id = input(f"Enter device ID {i+1} (leave empty to finish): ").strip()
        if device_id:
            devices.append(device_id)
        else:
            break

    # Add devices to Firestore under 'devices' subcollection
    for index, device_id in enumerate(devices, start=1):
        device_doc_ref = doc_ref_user.collection('devices').document(f'device{index}')
        device_doc_ref.set({'id': device_id})
        print(f"Added device {index}: {device_id}")

    print(f"Email '{email}' and devices added successfully to Firestore.")

if __name__ == "__main__":
    # Example usage:
    admin_email = "bted4389@gmail.com"
    add_email_as_admin(admin_email)
