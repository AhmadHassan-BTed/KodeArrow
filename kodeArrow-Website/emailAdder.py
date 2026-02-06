# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase
# cred = credentials.Certificate('kodearrow-server-firebase-adminsdk-9qxya-d2f88510eb.json')
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# def add_email_as_admin(email):

#     # Add the email to Firestore users collection
#     doc_ref_user = db.collection('users').document(email)
#     doc_user = doc_ref_user.get()
#     if doc_user.exists:
#         print(f"Email '{email}' already exists in Firestore users collection.")
#     else:
#         # Add the email to Firestore users collection
#         doc_ref_user.set({'email': email})
#         print(f"Added '{email}' to users collection.")

#     # Prompt user to enter up to 4 device IDs
#     devices = []
#     for i in range(4):
#         device_id = input(f"Enter device ID {i+1} (leave empty to finish): ").strip()
#         if device_id:
#             devices.append(device_id)
#         else:
#             break

#     # Add devices to Firestore under 'devices' subcollection
#     for index, device_id in enumerate(devices, start=1):
#         device_doc_ref = doc_ref_user.collection('devices').document(f'device{index}')
#         device_doc_ref.set({'id': device_id})
#         print(f"Added device {index}: {device_id}")

#     print(f"Email '{email}' and devices added successfully to Firestore.")

# if __name__ == "__main__":
#     # Example usage:
#     admin_email = "syedumais005@gmail.com"
#     add_email_as_admin(admin_email)
#########################################################################
# import firebase_admin
# from firebase_admin import credentials, firestore
# from datetime import datetime

# # Initialize Firebase
# cred = credentials.Certificate('kodearrow-server-firebase-adminsdk-9qxya-d2f88510eb.json')
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# def add_user(email, subscription_date_str):
#     # Parse the subscription date
#     try:
#         subscription_date = datetime.strptime(subscription_date_str, "%Y-%m-%d").date()
#     except ValueError:
#         print("Invalid date format. Please use YYYY-MM-DD.")
#         return

#     # Add the email to Firestore users collection if it doesn't already exist
#     doc_ref_user = db.collection('users').document(email)
#     doc_user = doc_ref_user.get()
#     if doc_user.exists():
#         print(f"Email '{email}' already exists in Firestore users collection.")
#     else:
#         # Add the email and subscription date to Firestore users collection
#         doc_ref_user.set({'email': email, 'subscription_date': subscription_date})
#         print(f"Added '{email}' to users collection with subscription date {subscription_date}.")

#     # Initialize placeholders for 4 devices if they don't exist
#     for i in range(1, 5):
#         device_doc_ref = doc_ref_user.collection('devices').document(f'device{i}')
#         device_doc = device_doc_ref.get()
#         if not device_doc.exists():
#             device_doc_ref.set({'id': f'device{i}'})
#             print(f"Added placeholder for device {i}")

#     print(f"Email '{email}' and placeholders for devices added successfully to Firestore.")

# if __name__ == "__main__":
#     # Example usage:
#     user_email = "ted@gmail.com"
#     subscription_date_str = datetime.today().strftime("%Y-%m-%d")
#     add_user(user_email, subscription_date_str)

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate('kodearrow-server-firebase-adminsdk-9qxya-d2f88510eb.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def add_user(email, subscription_date_str):
    # Parse the subscription date
    try:
        subscription_date = datetime.strptime(subscription_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Convert subscription_date to string
    subscription_date_str = subscription_date.strftime("%Y-%m-%d")

    # Add the email to Firestore users collection if it doesn't already exist
    doc_ref_user = db.collection('users').document(email)
    doc_user = doc_ref_user.get()
    if doc_user.exists:
        print(f"Email '{email}' already exists in Firestore users collection.")
    else:
        # Add the email and subscription date to Firestore users collection
        doc_ref_user.set({'email': email, 'subscription_date': subscription_date_str})
        print(f"Added '{email}' to users collection with subscription date {subscription_date_str}.")

    # Initialize placeholders for 4 devices if they don't exist
    # for i in range(1, 5):
    #     device_doc_ref = doc_ref_user.collection('devices').document(f'device{i}')
    #     device_doc = device_doc_ref.get()
    #     if not device_doc.exists:
    #         device_doc_ref.set({'id': f'device{i}'})
    #         print(f"Added placeholder for device {i}")

    # print(f"Email '{email}' and placeholders for devices added successfully to Firestore.")

if __name__ == "__main__":
    # Example usage:
    user_email = "bted0458@gmail.com"
    subscription_date_str = datetime.today().strftime("%Y-%m-%d")  # Use today's date in the correct format
    add_user(user_email, subscription_date_str)
