import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('kodearrow-server-firebase-adminsdk-9qxya-d2f88510eb.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def check_and_update(email, hardware_id):
    # Check if the email exists in Firestore users collection
    user_ref = db.collection('users').document(email)
    user_doc = user_ref.get()

    if user_doc.exists:
        # User exists, check devices
        devices_ref = user_ref.collection('devices')
        devices_query = devices_ref.get()

        if len(devices_query) >= 4:
            print("Maximum devices reached.")
        else:
            # Check if hardware ID already exists
            hardware_exists = False
            for device in devices_query:
                if device.to_dict().get('id') == hardware_id:
                    hardware_exists = True
                    break
            
            if hardware_exists:
                print("Hardware ID already exists. Activating premium.")
                create_premium_file()
            else:
                # Add hardware ID to Firestore
                device_data = {'id': hardware_id}
                devices_ref.document(f'device{len(devices_query) + 1}').set(device_data)
                print(f"Added hardware ID '{hardware_id}' to Firestore.")
                print("Activating premium.")
                create_premium_file()
    else:
        # User does not exist
        print("Email not registered.")

def create_premium_file():
    # Function to create the premium file
    premium_file_path = "PremiumUnlockDataFile.txt"
    with open(premium_file_path, "w") as file:
        file.write("premium Unlocked\n")

if __name__ == "__main__":
    # Example usage:
    email = "bted@gmail.com"
    hardware_id = "90884XD"

    check_and_update(email, hardware_id)
