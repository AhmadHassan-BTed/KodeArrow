import pyautogui
import keyboard
import os
from datetime import datetime
#import sys
import pystray
from PIL import Image
import webbrowser
from tkinter import messagebox
import platform
import subprocess
import wmi
import itertools
import firebase_admin
from firebase_admin import credentials, firestore
import requests  # Import requests library for network connectivity check
from customtkinter import *
import customtkinter as ctk
from plyer import notification
from dateutil.relativedelta import relativedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import time

pyautogui.PAUSE = 0.000001

windows = []

total_keyStrokes = 0
total_shortcuts = 0
total_runtime = 0
previous_time = time.time() 

def show_notification():
    notification.notify(
        title='KodeArrow in system tray',
        message='Right-Click KodeArrow icon to open',
        app_name='KodeArrow',
        timeout=0,  # Duration of the notification
        app_icon='icon.ico'  # Path to your icon file
    )

def initialize_firestore():
    try:
        cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "kodearrow-server",
        "private_key_id": "12f26b7c63d80d9d0901d9b8644b4f5ad12ebb28",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDGDu+3E6sI34Qw\nqAMOgp0D6fCmNtJmK0ESBFJyUrU38H6ZwtfnSHppnfFvvqbDXiqCCEKvc2dcXBmt\nBndUsXMPNsPv4fLJB30l8EQozr/ai1SsGoHFcZIYXwT0R6Ao5nWy49Ixj+URoBcy\nqfowR60JJMwn+a4KomEEd551f3RIWe/Ik/Oae0Hk3ONTdUGpZpHrN2WxCXSgk3zt\n2FiTZW+HEHyYYAF65XcX94asXpX1UeUMrpf02S8sI2/X/6PUEdGK5YfWhEE35uLH\n4oL62RSIk5b4eoJPC67+rDIDxeBUs3V/LJIn8AoxcW/FWMb1fwdZtZSW/yDqXV4L\nFGYWFwevAgMBAAECggEAFdw5LiJQGuscuogYykW1UeTEyHu9jkRQ6s2qUe76DIIR\nXyRH00HHLRgfOV+4JVEj7PU/cwEQU/vgY54WlrT9R50aVERCmVinwgO6aiyjtVny\njwpf72yBHQqDz/iF323MaOHHZewFcwQR+2gScri+iwdSN0lSId9ZSPZw+XQHYCLG\n/SA+3KXiQlfoHoVi+ZNbzwqJKAwDP5hy0UsvElkULXZLCA31zZZHd9gbhKv8osJa\ngXKbqA/IBF24v+hoO0r3KGj5m+OqEHD7FcGKs5EAxBzLT01dPmPSlDghDkH78HlM\nc6XyHuQaxI6FkBG/FtK/Dy5+fpe3fzAOlxe/vVjYUQKBgQD/2vvNfwEbwggqtweV\n84GAyj7R5x+OYP1Wy5E7fZ4zcoMDxGbm5LUjt3asO8YKxUtB8bSk5HvUcmoLLKfc\nLJy1fu0gv+Xi50lAcDsSrRbpPzy+6feVqh23O5EAZj4ZndhVfyUChALVxK+V1E/a\nfZh4jHqtEOq45Dr/RCApPytckQKBgQDGK5dDtzA4fvKTHfDvidtSILGBYe3jXDX1\nqFIbdLoIcYsQzUjTrepbH4pp55Rx9n+YBHIvs0DhMB2v2kiKCBFPGj7voZbHWfCN\n17qs1gYbmq7dJkm2oPajwqgOuVQZOsjmvVJDAdQNzsMV9hW2Pz7hQ9c8xv8vs+bQ\nsfSLXldAPwKBgDBS0eA8Lp9phFVdAGfH+Bu1FyxZ9NHVa8Pq6uFLloetByW9AJp3\nc+btDdL17y+1l8M6vZ2vMdwsR+8YXhPtsSNud6cJ14eFm4Y6LE4Ytw0SzoxYcFSq\nLrae34ItzWjVMTjkrL7O5CIv5eHsmbBwrE2IatspKMwG/0WbPl/L+IqhAoGAd99I\nadq23YXVAC7dXlh6hYxnM0dkmeJedZHy0M7j9VWRdIFo6zrJh4Nlu7gssF8WQYN2\n+umodk8ftg8JUA2fQsUyisupJD+AZpy3O/Ne0HXaDsYpUsK9TsPh2r46Y+SOQB0H\nVKcXeZ63nWI1Mf/B7ouV+Bq7pERje5wZu/A+QQsCgYAdpDWyLpkSX0SpmUIyL7RC\nUqwhhJ1y1hzh91Gqs9KPz53VzoBHcXT8VmTE4DJG8Nrm3RAxgu0ydmz5n9Fq4BUX\n7E/GIEzKaswgiDUkPHjJzDVF2hs2/5jqopCBK31PxH7jst0r7Xg02AYbSyU/pMqa\ndKmjzfzBS7WlXg06wn0JxA==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-9qxya@kodearrow-server.iam.gserviceaccount.com",
        "client_id": "102780777134400554469",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9qxya%40kodearrow-server.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        }
        )
    
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except Exception as e:
        if 'invalid_grant: Invalid JWT Signature' in str(e):
            messagebox.showinfo("Error", "Please update KodeArrow to the newest version")
            print("Please update KodeArrow to the newest version")
        else:
            messagebox.showinfo("Error", "Please update KodeArrow to the newest version")
            print(f"An error occurred: {e}")
db = initialize_firestore()

def check_internet_connection():
    # Check internet connectivity using a simple GET request to google.com
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False

def get_hardware_id():
    system = platform.system()
    if system == "Windows":

        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        return bios.SerialNumber
    elif system == "Darwin":  # macOS
        command = "ioreg -l | grep IOPlatformSerialNumber"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        serial_number = result.stdout.split('=')[-1].strip().strip('"')
        return serial_number
    elif system == "Linux":
        command = "cat /sys/class/dmi/id/product_uuid"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    else:
        raise NotImplementedError(f"Unsupported platform: {system}")

def encrypt_hardwareID(s):
    encrypted_chars = []
    for char in s:
        if char.isalnum():  # Check if the character is alphanumeric
            if char.isalpha():  # Check if the character is a letter
                if char.isupper():  # For uppercase letters
                    new_char_code = (ord(char) - ord('A') + 3) % 26 + ord('A')
                    encrypted_chars.append(chr(new_char_code))
                else:  # For lowercase letters
                    new_char_code = (ord(char) - ord('a') + 3) % 26 + ord('a')
                    encrypted_chars.append(chr(new_char_code))
            else:  # If the character is a digit
                new_char_code = (ord(char) - ord('0') + 3) % 10 + ord('0')
                encrypted_chars.append(chr(new_char_code))
    return ''.join(encrypted_chars)

# def decrypt_hardwareID(s):
#     # Shift each character's ASCII value back by 1
#     original = ''.join(chr(ord(char) - 1) for char in s)
#     return original

# def decrypt_hardwareID(s):
#     decrypted_chars = []
#     for char in s:
#         if char.isalnum():  # Check if the character is alphanumeric
#             if char.isalpha():  # Check if the character is a letter
#                 if char.isupper():  # For uppercase letters
#                     original_char_code = (ord(char) - ord('A') - 3) % 26 + ord('A')
#                     decrypted_chars.append(chr(original_char_code))
#                 else:  # For lowercase letters
#                     original_char_code = (ord(char) - ord('a') - 3) % 26 + ord('a')
#                     decrypted_chars.append(chr(original_char_code))
#             else:  # If the character is a digit
#                 original_char_code = (ord(char) - ord('0') - 3) % 10 + ord('0')
#                 decrypted_chars.append(chr(original_char_code))
#     return ''.join(decrypted_chars)


encrypted_hardware_id = "B4" + encrypt_hardwareID(get_hardware_id()) + "3TzD" + encrypt_hardwareID(encrypt_hardwareID(get_hardware_id())) + "u"

# Define the tray icon image and tooltip
icon_image_path = "icon.ico"
tooltip_text = "KodeArrow by Ahmad Hassan"
premium_file_path = f"{encrypted_hardware_id}.txt"

# Load the icon image and resize it to a suitable size for the tray (e.g., 16x16)
icon_image = Image.open(icon_image_path)
icon_image = icon_image.resize((16, 16))

# Path for the file to store data
usageData_file = "premium_Key_metadata.txt"

# Function to remove the hidden attribute before writing
def remove_hidden_attribute(file_path):
    try:
        # For Windows: Use subprocess to remove the hidden attribute without showing CMD window
        subprocess.check_call(["attrib", "-H", file_path], creationflags=0x08000000)
        print(f"Hidden attribute removed for '{file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove hidden attribute: {e}")

# Function to reapply the hidden attribute after writing
def add_hidden_attribute(file_path):
    try:
        # For Windows: Use subprocess to add the hidden attribute without showing CMD window
        subprocess.check_call(["attrib", "+H", file_path], creationflags=0x08000000)
        print(f"Hidden attribute added for '{file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add hidden attribute: {e}")

# Function to create a hidden file with initial values (if the file doesn't exist)
def create_hidden_file(file_path, total_keyStrokes=0, total_shortcuts=0, total_runtime=0):
    if not os.path.exists(file_path):
        # Initialize content with default values
        content = f"{total_keyStrokes}\n{total_shortcuts}\n{total_runtime}\n"
        
        try:
            with open(file_path, "w") as file:
                file.write(content)
            
            # Set the file as hidden based on the platform (Windows only)
            if platform.system() == "Windows":
                add_hidden_attribute(file_path)
            elif platform.system() in ["Darwin", "Linux"]:
                # For macOS and Linux: Prefix file name with a dot to hide it
                os.rename(file_path, f".{file_path}")
            else:
                raise NotImplementedError(f"Unsupported platform: {platform.system()}")
            
            print(f"Hidden file '{file_path}' created successfully.")
        
        except Exception as e:
            print(f"Failed to create hidden file '{file_path}': {e}")

# Function to write variables to the file
def write_to_file(file_path, total_keyStrokes, total_shortcuts, total_runtime):
    try:
        remove_hidden_attribute(file_path)
        
        temp_total_keyStrokes, temp_total_shortcuts, temp_total_runtime = read_from_file(usageData_file)

        with open(file_path, "w") as file:
            file.write(f"{total_keyStrokes+temp_total_keyStrokes}\n{total_shortcuts+temp_total_shortcuts}\n{total_runtime+temp_total_runtime}\n")
            
        add_hidden_attribute(file_path)
        
    except Exception as e:
        print(f"Failed to write to file '{file_path}': {e}")

# Function to read variables from the file
def read_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            
            # Check if the file has the expected number of lines
            if len(lines) != 3:
                raise ValueError("File has an unexpected number of lines.")
            
            # Read lines and ensure all lines contain valid integers
            total_keyStrokes = int(lines[0].strip())  # Convert the first line to an integer
            total_shortcuts = int(lines[1].strip())   # Convert the second line to an integer
            total_runtime = float(lines[2].strip())   # Convert the third line to a float (in case it's a decimal)
        
        return total_keyStrokes, total_shortcuts, total_runtime
    except FileNotFoundError:
        print("File not found. Initializing values to 0.")
        return 0, 0, 0
    except ValueError as e:
        print(f"Invalid data in file: {e}. Reinitializing values to 0.")
        return 0, 0, 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Reinitializing values to 0.")
        return 0, 0, 0

def process_user_data():
    create_hidden_file(usageData_file)

def upload_data_to_server(file_path):
    try:
        # Remove the hidden attribute from the file
        # remove_hidden_attribute(file_path)
        
        # Read usage data from the file
        temp_total_keyStrokes, temp_total_shortcuts, temp_total_runtime = read_from_file(file_path)

        add_hidden_attribute(file_path)
        # Fetch the email from the file and get the corresponding Firestore document
        doc_ref_user = db.collection('ControlGroup').document(find_email_in_file(premium_file_path))
        usage_ref = doc_ref_user.collection('usage').document('usage_data')

        # Fetch the existing usage data from Firestore
        usage_doc = usage_ref.get()

        if usage_doc.exists:
            # Extract the existing data
            existing_data = usage_doc.to_dict()
            
            # Update the existing data with new values
            existing_data['charactersTyped'] += temp_total_keyStrokes
            existing_data['kodeArrowHotkeys'] += temp_total_shortcuts
            existing_data['TotalUsageMinutes'] += temp_total_runtime
            
            # Save the updated data back to Firestore
            usage_ref.set(existing_data)
            print("Usage data updated successfully.")
            
            remove_hidden_attribute(file_path)
            # Reset the file only after successful upload
            with open(file_path, "w") as file:
                file.write(f"{0}\n{0}\n{0}\n")

            add_hidden_attribute(file_path)
        else:
            print("Usage document does not exist. Initialize it first.")

        # Reapply the hidden attribute to the file
        
        
    except Exception as e:
        print(f"Failed to write to file '{file_path}': {e}")


def run_async_upload_threaded(file_path):
    # Define a target function for the thread
    def target_function():
        try:
            remove_hidden_attribute(file_path)
            
            temp_total_keyStrokes, temp_total_shortcuts, temp_total_runtime = read_from_file(file_path)

            doc_ref_user = db.collection('ControlGroup').document(find_email_in_file(premium_file_path))
            usage_ref = doc_ref_user.collection('usage').document('usage_data')

            # Fetch the existing usage data
            usage_doc = usage_ref.get()

            if usage_doc.exists:
                # Extract the existing data
                existing_data = usage_doc.to_dict()
                
                # Update the existing data with new values
                existing_data['charactersTyped'] += temp_total_keyStrokes
                existing_data['kodeArrowHotkeys'] += temp_total_shortcuts
                existing_data['TotalUsageMinutes'] += temp_total_runtime
                
                # Save the updated data back to Firestore
                usage_ref.set(existing_data)
                print("Usage data updated successfully.")
                
                # Reset the file only after successful upload
                with open(file_path, "w") as file:
                    file.write(f"{0}\n{0}\n{0}\n")
            else:
                print("Usage document does not exist. Initialize it first.")

            # Reapply the hidden attribute to the file
            add_hidden_attribute(file_path)
            
        except Exception as e:
            print(f"Failed to upload data from file '{file_path}': {e}")

    # Start the target function in a separate thread
    thread = threading.Thread(target=target_function)
    thread.start()
    return thread

process_user_data()

#######################################################################################################


def is_premium():
    return os.path.exists(premium_file_path)

def find_email_in_file(path):
    found_email = None
    try:
        with open(path, "r") as file:
            for line in file:
                if line.strip().startswith("Email:"):
                    found_email = line.strip().split("Email:")[1].strip()
                    break
    except FileNotFoundError:
        # print(f"File '{path}' not found.")
        return
    except Exception as e:
        # print(f"Error reading file '{path}': {e}")
        return
    return found_email

def showMessage_subscriptionEnded(message):
    app = CTk()
    app.title("KodeArrow")
    app.iconbitmap("icon.ico")

    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()

    ctk.set_appearance_mode("Light")
    app.resizable(False, False)

    def closeWindow_andBuySubscription():
        webbrowser.open("ahmadhassan-bted.github.io/KodeArrow/payment.html")
        app.destroy()

    frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
    title = CTkLabel(master=frame1, text="KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
    subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
    labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 13))
    btn = CTkButton(master=frame1, text="Renew Subscription", width=180, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow_andBuySubscription)

    frame1.pack(fill=BOTH, expand=True)
    title.place(relx=0.5, rely=0.1, anchor="center")
    subtitle.place(relx=0.5, rely=0.2, anchor="center")

    w = 450
    h = 250
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))

    labelLocked.place(relx=0.5, rely=0.5, anchor="center")
    btn.place(relx=0.5, rely=0.80, anchor="center")

    app.mainloop()

def showMessage_versionEnded(message):
    app = CTk()
    app.title("KodeArrow")
    app.iconbitmap("icon.ico")

    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()

    ctk.set_appearance_mode("Light")
    app.resizable(False, False)

    def closeWindow_andBuySubscription():
        webbrowser.open("ahmadhassan-bted.github.io/KodeArrow/")
        app.destroy()

    frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
    title = CTkLabel(master=frame1, text="KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
    subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
    labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 13))
    btn = CTkButton(master=frame1, text="Download New Version", width=180, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow_andBuySubscription)

    frame1.pack(fill=BOTH, expand=True)
    title.place(relx=0.5, rely=0.1, anchor="center")
    subtitle.place(relx=0.5, rely=0.2, anchor="center")

    w = 450
    h = 250
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))

    labelLocked.place(relx=0.5, rely=0.5, anchor="center")
    btn.place(relx=0.5, rely=0.80, anchor="center")

    app.mainloop()

#Function to show the initial instructions and key combinations

def showMessage():
    app = CTk()
    app.title("KodeArrow")
    app.iconbitmap("icon.ico")
    windows.append(app)
    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()

    ctk.set_appearance_mode("Light")
    app.resizable(False, False)

    def closeWindow():
        show_notification()
        app.destroy()

    def changeMessage():
        if is_premium():
            labelUnlocked.destroy()
            showMore.place(relx=0.5, rely=0.5, anchor="center")
            btnShowMore.destroy()
        else:
            labelLocked.destroy()
            showMore.place(relx=0.5, rely=0.471, anchor="center")
            showLock.place(relx=0.5, rely=0.48, anchor="center")
            padlockText.place(relx=0.5, rely=0.75, anchor="center")
            btnShowMore.destroy()

    message = (
        "Thank you for using KodeArrow, a product of ByTed Technologies\n\n"
        "Alt + I\n(Arrow 🔒 Up)\n\n"
        "Alt + J\t\t\t\tAlt + L\n(Arrow Left)\t\t\t(Arrow Right)\n\n"
        "Alt + K\n(Arrow 🔒 Down)\n\n"
        "\"Right click KodeArrow icon in System Tray to access menu\"\nNote: Please buy Premium version to unlock locked keys"
    )

    messageUnlocked = (
        "Thank you for using KodeArrow, a product of ByTed Technologies\n\n"
        "Alt + I\n(Arrow Up)\n\n"
        "Alt + J\t\t\t\tAlt + L\n(Arrow Left)\t\t\t(Arrow Right)\n\n"
        "Alt + K\n(Arrow Down)\n\nRemember: Right click KodeArrow icon in System Tray to access menu"
    )

    showMoreMessage = (
        " Thank you for using KodeArrow, a product of ByTed Technologies\n\n\n"
        "{:<26} {:<26} {:<26} {:<26} {:<0}\n"
        # "{:19} {:<24} {:<22} {:<24} {:<0}\n\n\n\n"
        "   {:20} {:<25} {:<24} {:<22} {:0}\n\n\n\n"
        "{:<26} {:<26} {:<26} {:<26} {:<0}\n"
        "{:<18} {:<18} {:<18} {:<18} {:<0}\n"
    ).format(
            "Alt + U", "Alt + I", "Alt + O", "Alt + P", "Alt + [",
            "(Home)", "(Arrow Up)", "(End)", "(Delete)", "(Page Up)",
            "Alt + J", "Alt + K", "Alt + L", "Alt + ;", "Alt + '",
            "(Arrow Left)", "(Arrow Down)", "(Arrow Right)", "(Backspace)", "(Page Down)"
    )

    frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
    title = CTkLabel(master=frame1, text="Welcome to KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
    subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
    labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 12))
    labelUnlocked = CTkLabel(master=frame1, text=messageUnlocked, bg_color="white", text_color="black", font=("Bahnschrift", 12))
    showMore = CTkLabel(master=frame1, text=showMoreMessage, bg_color="white", text_color="black", font=("Bahnschrift", 12))
    btn = CTkButton(master=frame1, text="Ok", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow)
    btnShowMore = CTkButton(master=frame1, text="➜", width=30, height=15, corner_radius=1, fg_color="white",text_color="#00207f", hover_color="white", bg_color="white", 
    command=changeMessage, font=("Arial", 24))
    showLock = ctk.CTkLabel( master=frame1, text="🔒", bg_color="transparent", text_color="#00207f", font=("Bahnschrif", 50, "bold"))
    padlockText = ctk.CTkLabel( master=frame1, text="These services are premium locked", bg_color="transparent", text_color="black", font=("Bahnschrif", 12, "bold")
)

    frame1.pack(fill=BOTH, expand=True)
    title.place(relx=0.5, rely=0.1, anchor="center")
    subtitle.place(relx=0.5, rely=0.164, anchor="center")

    if is_premium():
        w = 480
        h = 350
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))
        labelUnlocked.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.87, anchor="center")
        btnShowMore.place(relx=0.9, rely=0.87, anchor="center")
    else:
        w = 480
        h = 360
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        labelLocked.place(relx=0.5, rely=0.51, anchor="center")
        btn.place(relx=0.5, rely=0.88, anchor="center")
        btnShowMore.place(relx=0.9, rely=0.88, anchor="center")

    app.mainloop()

# Define the function to open the URL
def open_url():
    webbrowser.open("bted.wuaze.com/")
    webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")

def open_url_buy():
    webbrowser.open("ahmadhassan-bted.github.io/KodeArrow/")

def create_hidden_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        
        # Try to set the hidden attribute based on the platform
        if platform.system() == "Windows":
            # Windows: Use ctypes to set hidden attribute
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
        elif platform.system() == "Darwin":
            # macOS: Prefix file name with a dot to hide it
            os.rename(file_path, f".{file_path}")
        elif platform.system() == "Linux":
            # Linux: Prefix file name with a dot to hide it
            os.rename(file_path, f".{file_path}")
        else:
            raise NotImplementedError(f"Unsupported platform: {platform.system()}")
        
        #print(f"Hidden file '{file_path}' created successfully.")
        
    except Exception as e:
        # print(f"Failed to create hidden file '{file_path}': {e}")
        return

# file_path = "systemCompatibility.txt"

def unlock_functionality():
    if is_premium():
        #print("Unlock Full Functionality", "Already unlocked (Paid version)")
        return True
    else:
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap("icon.ico")

        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()

        w = 450
        h = 250
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        ctk.set_appearance_mode("Light")
        app.resizable(False, False)

        frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
        title = CTkLabel(master=frame1, text="Welcome to KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
        subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
        label = CTkLabel(master=frame1, text="Please enter your Email", bg_color="white", text_color="black", font=("Bahnschrift", 14))
        field = CTkEntry(master=frame1, placeholder_text="Email", width=350, height=40)

        frame1.pack(fill=BOTH, expand=True)
        title.place(relx=0.5, rely=0.1, anchor="center")
        subtitle.place(relx=0.5, rely=0.2, anchor="center")
        label.place(relx=0.289, rely=0.4, anchor="center")
        field.place(relx=0.5, rely=0.55, anchor="center")
   

        def submit_key():
            email = field.get()
            hardware_id = get_hardware_id()

            if check_and_update(email, hardware_id):
                messagebox.showinfo("Congratulations", "Premium Unlocked")
                app.destroy()
 
            create_menu()
    
        btn = CTkButton(master=frame1, text="Submit", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#000d34", bg_color="white", command=submit_key)
        btn.place(relx=0.5, rely=0.79, anchor="center")
        app.mainloop()

def check_and_update(email, hardware_id):

    content = """YOUR PREMIUM UNLOCK IS UNLOCKED
                             
                             (((                                                
                             (((((((////                                        
                             (((((((((////                                      
                                   (((((///                                     
                                    ((((((/                                     
                                     (((((((                                    
                                     (((((((                                    
                                     (((((((                                    
                                     (((((((                                    
                                     (((((((                                    
                                     ###((((                                    
                                     #####((                                    
                                     #######                                    
                                      #######                                   
                                      ########            ##((                  
                                        ########          ####(((((((           
      THANKS FOR BUYING KODEARROW         ##########      ####   ((((((((((     
[]][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][      @@@@@@@@@@@ 
                                         ]]#########      &&&&&&&&&&&@@@        
                                        ]]]]]##           &&&&&&&&               
                                      ]]]]]]]             &&&&                    
                                     ]]]]]]%                                    
                                     &]]]]]]                                    
                                     &&&]]]]                                    
                                     &&&&&]]                                    
                                     &&&&&&&                                    
                                     &&&&&&&                                    
                                     &&&&&&&                                    
                                    @@@&&&&                                     
                             @@@@@@@@@@@@@&                                     
                             @@@@@@@@@@@@                                       
                             @@@@@@@@@@@                                       
                                 
CAUTION!
DO NOT MOVE THIS FILE UNDER ANY CIRCUMSTANCES.
DO NOT CHANGE THE DIRECTORY OF THIS FILE.
KEEP THE FILE IN THE SAME FOLDER.
DO NOT SHARE THIS FILE ACROSS ANY OTHER DEVICES.

VIOLATION OF ANY OF THESE INSTRUCTIONS MAY LEAD TO THE USER BEING HELD LIABLE FOR LEGAL ACTION.

Copyright© 2023. Ahmad Hassan(B-TED)
Project KodeArrow

For User:
"""

    # Check internet connectivity
    if not check_internet_connection():
        messagebox.showinfo("Error", "Please check your internet connection again.")
        return False
    
    # Check if the email exists in Firestore users collection
    user_ref = db.collection('ControlGroup').document(email)
    user_doc = user_ref.get()

    if user_doc.exists:
        # User exists, check devices
        devices_ref = user_ref.collection('devices')
        devices_query = devices_ref.get()
        subscription_date_str = user_doc.get('subscription_date')
        subscription_date = datetime.strptime(subscription_date_str, '%Y-%m-%d')

        # Get today's date
        today = datetime.today()

        # Compare dates
        if today >= subscription_date:
            # print("Email exists but the subscription period has expired. Deleting premium file.")
            showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us 💙 and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
            return False

        hardware_exists = False

        # for device in devices_query:
        #     if device.to_dict().get('id') == hardware_id or device.to_dict().get('id') == 'TrialVersion' :
        #         print(device.to_dict().get('id'))
        #         hardware_exists = True
        #         break
        for device in devices_query:
            if device.to_dict().get('id') == hardware_id or device.to_dict().get('id') == "TrailVersion":
                # Print the device id from the document
                print("this ran")
                hardware_exists = True
                break

        if hardware_exists:
                # print("Hardware ID already exists. Activating premium.")
                content += f"\n\nEmail: {email}\n"
                create_hidden_file(premium_file_path, content)
                return True

        elif len(devices_query) >= 1:
            messagebox.showinfo("Error", "Maximum devices reached")
            return False
        
        else:
                device_data = {'id': hardware_id}
                devices_ref.document(f'device{len(devices_query) + 1}').set(device_data)
                # print(f"Added hardware ID '{hardware_id}' to Firestore.")
                # print("Activating premium.")
                create_hidden_file(premium_file_path, content)
                return True
    else:
        # print("Email not registered.")
        messagebox.showinfo("Registration not Found", "Registration not Found: Please check your email")
        return False

############################################################################################################3
# Function to create the tray icon menu
def create_menu():
    global menu, icon
    menu = [
        pystray.MenuItem('Created by Ahmad Hassan', open_url),
    ]

    if is_premium():
        pass  # If premium, do not show the "Buy for $2" and "Unlock Full Functionality" options
        menu.append(pystray.MenuItem('Visit KodeArrow', open_url_buy, default=True))
    else:
        menu.append(pystray.MenuItem('Buy here for $2', open_url_buy, default=True))
        menu.append(pystray.MenuItem('Already bought? Unlock Here', unlock_functionality))
    
    menu.append(pystray.MenuItem('Exit', lambda icon, item: exit_program()))  # Add the Exit option to the menu
    
    # Update the icon with the new menu
    icon.menu = pystray.Menu(*menu)

# Create the initial menu
menu = []  # Define an empty menu
icon = pystray.Icon("KodeArrow by Ahmad Hassan", icon=icon_image, title=tooltip_text, menu=menu)
create_menu()
# Function to exit the program
def exit_program():
    if(check_internet_connection()):
        upload_data_to_server(usageData_file)
    icon.stop()
    sys.exit()

##############################################################################################
#### this will check on startup, if the user is valid, and if we need a new version or not####
##############################################################################################

def validate_email_info_of_the_user():

    if os.path.exists(premium_file_path):
        email = find_email_in_file(premium_file_path)
        if email:
            print(f"Found email in file: {email}")

            # Check if the email exists in Firestore users collection
            user_ref = db.collection('ControlGroup').document(email)
            user_doc = user_ref.get()

            if user_doc.exists:
                # Get the subscription date
                subscription_date_str = user_doc.get('subscription_date')
                if subscription_date_str:
                    subscription_date = datetime.strptime(subscription_date_str, '%Y-%m-%d')

                    # Calculate one year later
                    # one_year_later = subscription_date.replace(year=subscription_date.year + 1)
                    six_months_later = subscription_date + relativedelta(months=1)
                    print(six_months_later)
                    # Get today's date
                    today = datetime.today()

                    # Compare dates
                    if today < six_months_later:
                        # print("Email exists in the Firestore database and is still within the subscription period. No action needed.")
                        return
                    else:
                        # print("Email exists but the subscription period has expired. Deleting premium file.")
                        os.remove(premium_file_path)
                        showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us 💙 and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
                else:
                    # print("Subscription date not found in Firestore. Deleting premium file.")
                    os.remove(premium_file_path)
                    showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us 💙 and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
            else:
                # print("Email does not exist in the Firestore database. Deleting premium file.")
                os.remove(premium_file_path)
                showMessage_subscriptionEnded("A change in permission has been noticed\nPlease re-enter your email to activate premium version")
        else:
            # print("Email not found in the premium file. Deleting premium file.")
            os.remove(premium_file_path)
            showMessage_subscriptionEnded("A change in permission has been noticed\nPlease re-enter your email to activate premium version")
    else:
        # print("Premium file does not exist. No action needed.")
        return

def close_windows():
    for window in windows[:]:  # Use a copy of the list to avoid modification issues
        if window.winfo_exists():
            window.destroy()
            windows.remove(window)
    
def statup_configuration():
        admin_ref = db.collection('admins').document('StartUp_Configurations').collection("version_2.0_research").document('stats')
        doc = admin_ref.get()
        doc_data = doc.to_dict()
        status = doc_data.get('status_flag_2.0_research')
        message = doc_data.get('message_2.0_research')
        if status:
            showMessage_versionEnded("message")
            # messagebox.showinfo("Error", message)
            print("stoping icon")
            icon.stop()
            print("icon stopped\n")
            # close_windows()
            print("removing windows")
            threading.Thread(target=close_windows, daemon=True).start()
            if os.path.exists(premium_file_path):
                os.remove(premium_file_path)
            exit_program()
            
        else:
            validate_email_info_of_the_user()

def start_check_and_update():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_check_and_update_with_timeout())
    loop.close()

async def run_check_and_update_with_timeout():
    with ThreadPoolExecutor() as executor:
        try:
            await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(executor, statup_configuration), timeout=30)
        except asyncio.TimeoutError:
            messagebox.showinfo("Error", "The current version has expired\nPlease update KodeArrow to the newest version")
            os.remove(premium_file_path)
            sys.exit()

# Running the check_and_update function in a separate thread

thread = threading.Thread(target=start_check_and_update)

if check_internet_connection():
    thread.start()

##############################################################################################
# Show the initial instructions when the program starts
# showMessage()
threading.Thread(target=showMessage, daemon=True).start()
##############################################################################################

def hehe():
    return True

def updateData():
        global total_shortcuts
        global total_keyStrokes
        total_keyStrokes -= 1
        total_shortcuts += 1
        # print(f"Total Shortcuts: {total_shortcuts}")
        

# Define the hotkey event hooks and suppress the default behavior (suppress=True)
def left_arrow():
    keyboard.add_hotkey('alt+left', hehe, suppress=True)
    pyautogui.press('left')       # Full functionality for the paid version
    updateData()
    keyboard.remove_hotkey('alt+left')

def down_arrow():
    if is_premium():
        keyboard.add_hotkey('alt+down', hehe, suppress=True)
        pyautogui.press('down')  # Full functionality for the paid version
        updateData()
        keyboard.remove_hotkey('alt+down')
    
    else:
        return

def up_arrow():
    if is_premium():
        keyboard.add_hotkey('alt+up', hehe, suppress=True)
        pyautogui.press('up')       # Full functionality for the paid version
        updateData()
        keyboard.remove_hotkey('alt+up')
    else:
        return

def right_arrow():
    keyboard.add_hotkey('alt+right', hehe, suppress=True)
    pyautogui.press('right')
    updateData()
    keyboard.remove_hotkey('alt+right')

def page_up_key():
    if is_premium():
        keyboard.add_hotkey('alt+pageup', hehe, suppress=True)
        pyautogui.press('pageup')
        updateData()
        keyboard.remove_hotkey('alt+pageup')
    else:
        return

def page_down_key():
    if is_premium():
        keyboard.add_hotkey('alt+pagedown', hehe, suppress=True)
        pyautogui.press('pagedown')
        updateData()
        keyboard.remove_hotkey('alt+pagedown')
    else:
        return

def end_key():
    if is_premium():
        keyboard.add_hotkey('alt+end', hehe, suppress=True)                                 
        pyautogui.press('end')
        updateData()
        keyboard.remove_hotkey('alt+end')
    else:
        # print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version
        return

def home_key():
    if is_premium():
        keyboard.add_hotkey('alt+home', hehe, suppress=True)
        pyautogui.press('home')
        updateData()
        keyboard.remove_hotkey('alt+home')
    else:
        #print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version
        return

def backspace_key():
    if is_premium():
        keyboard.add_hotkey('alt+backspace', hehe, suppress=True)
        pyautogui.press('backspace')
        updateData()
        keyboard.remove_hotkey('alt+backspace')
    else:
        #print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version
        return
    
def delete_key():
    if is_premium():
        keyboard.add_hotkey('alt+delete', hehe, suppress=True)
        pyautogui.press('delete')
        updateData()
        keyboard.remove_hotkey('alt+delete')
    else:
        #print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version
        return

key_actions = {
    'i': up_arrow,
    'j': left_arrow,
    'k': down_arrow,
    'l': right_arrow
}

# Function to handle combinations
def handle_combination(*keys):
    for key in keys:
        key_actions[key]()  # Call the respective function for each key

# Add hotkeys for all combinations
keys = ['i', 'j', 'k', 'l']

# Single key combinations
for key in keys:
    keyboard.add_hotkey(f'alt+{key}', handle_combination, args=(key,), suppress=True)

# Two key combinations
for combo in itertools.permutations(keys, 2):
    keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}', handle_combination, args=combo, suppress=True)

# Three key combinations
for combo in itertools.permutations(keys, 3):
    keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}+{combo[2]}', handle_combination, args=combo, suppress=True)

# Four key combinations
for combo in itertools.permutations(keys, 4):
    keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}+{combo[2]}+{combo[3]}', handle_combination, args=combo, suppress=True)

keyboard.add_hotkey('alt+u', home_key, suppress=True)
keyboard.add_hotkey('alt+o', end_key, suppress=True)
keyboard.add_hotkey('alt+p', delete_key, suppress=True)
keyboard.add_hotkey('alt+;', backspace_key, suppress=True)
keyboard.add_hotkey('alt+[', page_up_key, suppress=True)
keyboard.add_hotkey("alt+'", page_down_key, suppress=True)

multiplier = 20;

def calculate_user_data():
        global total_keyStrokes
        global total_shortcuts
        global multiplier
        global previous_time

        total_keyStrokes += 1
        if(total_keyStrokes > multiplier):
            current_time = time.time() 
            time_interval = current_time - previous_time 
            previous_time = current_time

            write_to_file(usageData_file, total_keyStrokes, total_shortcuts, time_interval/60)

            if(check_internet_connection()):
                run_async_upload_threaded(usageData_file)

            total_shortcuts = 0
            total_keyStrokes = 0

def increment_total_keyStrokes(event):
        if event.event_type == 'down':
             calculate_user_data()

        print(f"Total keys pressed: {total_keyStrokes}")

keyboard.hook(increment_total_keyStrokes)
############################################################################################


if(check_internet_connection()):
    run_async_upload_threaded(usageData_file)

icon.run()
thread.join()
## now implement that, when the person gets online, it uplaods the data

## scxvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzcvzcvzcvxzxcvzxvczxcvzxcvzvzvczcvzcxvzcxvzcvzxcvzxcvzxcvzxcvzcvasdfasdfasdfasdfasdfasdfasdfasdfsadfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfadsfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfasdfasdfasdfasdfasdfasdfadsfasdfasdfasdfadsfadsfadfadfadfadf
