from cryptography.fernet import Fernet
import json

# Function to generate a key and save it into a file
def generate_key():
    key = Fernet.generate_key()
    print(key)
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

generate_key()
# # Function to load the key from the current directory named `secret.key`
# def load_key():
#     return open("secret.key", "rb").read()

# # Function to encrypt a .json file
# def encrypt_file(file_name, key):
#     fernet = Fernet(key)
    
#     with open(file_name, "rb") as file:
#         original_file = file.read()
    
#     encrypted_file = fernet.encrypt(original_file)
    
#     with open(file_name + ".enc", "wb") as encrypted_file_obj:
#         encrypted_file_obj.write(encrypted_file)

# # Function to decrypt a .json file
# def decrypt_file(encrypted_file_name, key):
#     fernet = Fernet(key)
    
#     with open(encrypted_file_name, "rb") as enc_file:
#         encrypted_file = enc_file.read()
    
#     decrypted_file = fernet.decrypt(encrypted_file)
    
#     with open(encrypted_file_name.replace(".enc", ""), "wb") as dec_file:
#         dec_file.write(decrypted_file)

# # Generate and save the key (only run once)
# generate_key()

# # Load the key
# key = load_key()

# # Encrypt the file
# encrypt_file("kodearrow-website-167ead05474a.json", key)

# # Decrypt the file
# decrypt_file("kodearrow-website-167ead05474a.json.enc", key)
