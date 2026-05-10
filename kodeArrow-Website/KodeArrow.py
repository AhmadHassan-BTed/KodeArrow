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

pyautogui.PAUSE = 0.000

#cred = credentials.Certificate('kodearrow-server-firebase-adminsdk-9qxya-d2f88510eb.json')

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "kodearrow-server",
  "private_key_id": "d2f88510eb7335c71b35124c039eecb9bd4434d1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC99K1a6/W9q/K6\nlm2Kbj7ambAFIewI/Jgb3U4aOJxWTETmD8+yHC/ZjVq/fvetawiqwlwv66CeAfRa\nsSKij182e/f29bR0t3HefJ6HD7H3ctwnGyed0dr+SNyks/GT9f7YOaYJEMu+R4NY\nUC8pUtZs2xGdOYdIZNOdWtjQ/XgyMOctpUwOc33RluprVREp82BPfwQBvUnCArj6\n2xikrRBmyTSj9lWKB1C/yCV6ujTC4K6l3cQ8qUrOgaSy5niCTKKJfdK4QH8orqvI\noutIDeGFTsohZcAcO1KKjvc+kgTh1W02Ec98dz+CIzraOQmtQMUfU3byrdqarb8y\nf7aSuT7bAgMBAAECggEAWTLIpr3PrunL+NdDh/Id/LuXfsl/k3a9nLQOhVyY+SMm\nZVv+XTZEN+XbO7oM5vewYbMT5ALC8P+c9WthhrFJdgW/mk2ll/s+csnVDToPCVH7\n1Dc5oq/VJHwldAf1hFPLAFENyQsEiYz+Pd2lT8PQ4dv7CPfnMVT7U9RBpN2pb/Nc\nWNNf6YlWsUoSmYRz6GGvYvItOVJlQh47Q2Kx/X0hqmX3FD8/4JgrQZYT6R4g4E1o\neYFpK+XSR5+N13xbR9ZN1MifQT31F43cNhirGhTq1jzC71oX7kUaNhReRUGGGU6F\nzpzTshulwIlMkvC/wWMU+ut4kCrWpDwShv9NB3z95QKBgQDqMN1CIJ+JC7SH7V2x\ngS/IBGz9o1smXVLpVWXcJtOeUbvm3kZXXHviu5ZtRV9k+qSOz7iGUTewZyM508br\npR9MiBdnMTHlgInaQe40xT+hjfzlyNntFwfTCpv0Z/bloEFxsXHgT3HNe5dfRJo2\nU8HpTddSvmTJTHXzAzUUMmUkXQKBgQDPpT5BmQBYqD9HePqX9OHkoKfR+WHjVgRc\nswNvX/J/+ViKlVmDDlQsw2s51LvxjD9LrAVq7c96DrX4hAqgdw/MqTC3CVHrb8cN\nrZzmPJjDGUzqgT2MXh0t8WbILcg8JNHZ1+WP9kUL1rKL6UtVpo9nyWD+b89PaVJ/\nf9ZrXgc8lwKBgHJICCDV5KQu5xkRtxAA171Gk50uUzOkhOpCdyN4evoeLpCZ1T+a\nbQYWvnByUvvm59ic+xHonkFiAymb881YVa62Fp2PvyaclCjC1ahAvS1sKYZEfjwZ\nagMNgU9CUJR7oJQHoGdyvTkl35do1cw/ETh1eOby7CHjQwekgAlsEjktAoGBAJQt\np6/IL6cU6ZNnkey+pDUzMI93F5PT3mkIlnr0TWll1vmOesI7h3YqPmqWlUhafRDT\nQUp9SoIf3VvrXmoEjRHP6yOzUvJgYfww2La0p48SjwEKGZIB13DhxCc2BJ5m6Bo9\nJ2UEqWE5ZVDSux/0LII0AzOPNrHEx0qVP75+60shAoGAO2AMVM4c1d1DrfGeUThF\nDrLfoNrRpMGQvi704hN7q3nbbza/ku6f+1c3XmOKNgTsSpOb1rVhm91c1Vozhu8Y\nqvRaTz2KRwxd4v6tJhLyfisP5CwxHi+/sLtL9Pb9H+bBeoJEBA49oE3hbyj+utjm\nU5XhilsACK0pg84K7ueKgjo=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-9qxya@kodearrow-server.iam.gserviceaccount.com",
  "client_id": "102780777134400554469",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9qxya%40kodearrow-server.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)
db = firestore.client()


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

# def encrypt_hardwareID(s):
#     # Shift each character's ASCII value by 7
#     altered = ''.join(chr(ord(char) + 3) for char in s)
#     return altered

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

def decrypt_hardwareID(s):
    # Shift each character's ASCII value back by 1
    original = ''.join(chr(ord(char) - 1) for char in s)
    return original

encrypted_hardware_id = "B4" + encrypt_hardwareID(get_hardware_id()) + "3TzD" + encrypt_hardwareID(encrypt_hardwareID(get_hardware_id())) + "u"

def check_internet_connection():
    # Check internet connectivity using a simple GET request to google.com
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False

# Define the tray icon image and tooltip
icon_image_path = "icon.ico"
tooltip_text = "KodeArrow by Ahmad Hassan"
premium_file_path = f"{encrypted_hardware_id}.txt"

# Load the icon image and resize it to a suitable size for the tray (e.g., 16x16)
icon_image = Image.open(icon_image_path)
icon_image = icon_image.resize((16, 16))

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
        print(f"File '{path}' not found.")
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
    return found_email

#######################################################################################


def showMessage_subscriptionEnded(message):
    app = CTk()
    app.title("KodeArrow")
    app.iconbitmap("icon.ico")

    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()

    ctk.set_appearance_mode("Light")
    app.resizable(False, False)

    def closeWindow_andBuySubscription():
        webbrowser.open("kodearrow.wuaze.com/payment.html")
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

#######################################################################################

def validate_email_info_of_the_user():
    if os.path.exists(premium_file_path):
        email = find_email_in_file(premium_file_path)
        if email:
            print(f"Found email in file: {email}")

            # Check if the email exists in Firestore users collection
            user_ref = db.collection('users').document(email)
            user_doc = user_ref.get()

            if user_doc.exists:
                # Get the subscription date
                subscription_date_str = user_doc.get('subscription_date')
                if subscription_date_str:
                    subscription_date = datetime.strptime(subscription_date_str, '%Y-%m-%d')

                    # Calculate one year later
                    one_year_later = subscription_date.replace(year=subscription_date.year + 1)

                    # Get today's date
                    today = datetime.today()

                    # Compare dates
                    if today < one_year_later:
                        print("Email exists in the Firestore database and is still within the subscription period. No action needed.")
                        return
                    else:
                        print("Email exists but the subscription period has expired. Deleting premium file.")
                        showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us 💙 and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
                        os.remove(premium_file_path)
                else:
                    print("Subscription date not found in Firestore. Deleting premium file.")
                    showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us 💙 and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
                    os.remove(premium_file_path)
            else:
                print("Email does not exist in the Firestore database. Deleting premium file.")
                showMessage_subscriptionEnded("Naughty Naughty, Don't change the File, I've told you!\nnow go and enter your email again")
                os.remove(premium_file_path)
        else:
            print("Email not found in the premium file. Deleting premium file.")
            showMessage_subscriptionEnded("Naughty Naught, Don't change the File, I've told you!\nnow go and enter your email again")
            os.remove(premium_file_path)
    else:
        print("Premium file does not exist. No action needed.")

# Example usage:
if check_internet_connection():
    print("entering in validation section")
    validate_email_info_of_the_user()
    
# def is_premium():  #a function to find %encrypted_hardware_id% found in any file name
#     # List all files in the current directory
#     files = os.listdir('.')
#     # Check if any file contains the specified substring in its name
#     for file in files:
#         if premium_file_path in file:
#             return 1
#     return 0

#Function to show the initial instructions and key combinations
def showMessage():
    app = CTk()
    app.title("KodeArrow")
    app.iconbitmap("icon.ico")

    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()

    ctk.set_appearance_mode("Light")
    app.resizable(False, False)

    def closeWindow():
        app.destroy()

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
        "Alt + K\n(Arrow Down)\n\n\"Right click KodeArrow icon in System Tray to access menu\""
    )

    frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
    title = CTkLabel(master=frame1, text="Welcome to KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
    subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
    labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 12))
    labelUnlocked = CTkLabel(master=frame1, text=messageUnlocked, bg_color="white", text_color="black", font=("Bahnschrift", 12))
    btn = CTkButton(master=frame1, text="Ok", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow)

    frame1.pack(fill=BOTH, expand=True)
    title.place(relx=0.5, rely=0.1, anchor="center")
    subtitle.place(relx=0.5, rely=0.164, anchor="center")

    if is_premium():
        w = 450
        h = 340
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        labelUnlocked.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.87, anchor="center")
    else:
        w = 450
        h = 360
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        labelLocked.place(relx=0.5, rely=0.51, anchor="center")
        btn.place(relx=0.5, rely=0.88, anchor="center")

    app.mainloop()

# Show the initial instructions when the program starts
showMessage()

# Define the function to open the URL
def open_url():
    webbrowser.open("bted.wuaze.com/")

def open_url_buy():
    webbrowser.open("kodearrow.wuaze.com/")

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
        
        print(f"Hidden file '{file_path}' created successfully.")
        
    except Exception as e:
        print(f"Failed to create hidden file '{file_path}': {e}")

# file_path = "systemCompatibility.txt"

def unlock_functionality():
    if is_premium():
        print("Unlock Full Functionality", "Already unlocked (Paid version)")
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
    user_ref = db.collection('users').document(email)
    user_doc = user_ref.get()

    if user_doc.exists:
        # User exists, check devices
        devices_ref = user_ref.collection('devices')
        devices_query = devices_ref.get()
        subscription_date_str = user_doc.get('subscription_date')
        subscription_date = datetime.strptime(subscription_date_str, '%Y-%m-%d')

        # Calculate one year later
        one_year_later = subscription_date.replace(year=subscription_date.year + 1)

        # Get today's date
        today = datetime.today()

        # Compare dates
        if today >= one_year_later:
            print("Email exists but the subscription period has expired. Deleting premium file.")
            showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us 💙 and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
            return False

        hardware_exists = False
        for device in devices_query:
            if device.to_dict().get('id') == hardware_id:
                hardware_exists = True
                break
        
        if hardware_exists:
                print("Hardware ID already exists. Activating premium.")
                content += f"\n\nEmail: {email}\n"
                create_hidden_file(premium_file_path, content)
                return True

        elif len(devices_query) >= 4:
            messagebox.showinfo("Error", "Maximum devices reached")
            return False
        
        else:
                device_data = {'id': hardware_id}
                devices_ref.document(f'device{len(devices_query) + 1}').set(device_data)
                print(f"Added hardware ID '{hardware_id}' to Firestore.")
                print("Activating premium.")
                create_hidden_file(premium_file_path, content)
                return True
    else:
        print("Email not registered.")
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
    icon.stop()
    sys.exit()
# Define the hotkey event hooks and suppress the default behavior (suppress=True)
def left_arrow():
    pyautogui.press('left')

def down_arrow():
    if is_premium():
        pyautogui.press('down')  # Full functionality for the paid version
    else:
        print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version

def up_arrow():
    if is_premium():
        pyautogui.press('up')       # Full functionality for the paid version
    else:
        print("Limited Functionality", "Up arrow (Free version)") # Limited functionality for the free version

def right_arrow():
    pyautogui.press('right')

def page_up_key():
    if is_premium():
        pyautogui.press('pageup')  # Full functionality for the paid version
    else:
        print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version

def page_down_key():
    if is_premium():
        pyautogui.press('pagedown')  # Full functionality for the paid version
    else:
        print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version

def end_key():
    if is_premium():
        pyautogui.press('end')  # Full functionality for the paid version
    else:
        print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version

def home_key():
    if is_premium():
        pyautogui.press('home')  # Full functionality for the paid version
    else:
        print("Limited Functionality", "Down arrow (Free version)")   # Limited functionality for the free version


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

# keyboard.add_hotkey('alt+shift+i', page_up_key, suppress=True)
# keyboard.add_hotkey('alt+shift+j', page_down_key, suppress=True)
# keyboard.add_hotkey('alt+shift+l', end_key, suppress=True)
# keyboard.add_hotkey('alt+shift+k', home_key, suppress=True)

# Run the tray icon application
icon.run()