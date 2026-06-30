import os
from datetime import datetime
from tkinter import messagebox
from dateutil.relativedelta import relativedelta
from kode_arrow.utils.file import create_hidden_file
from kode_arrow.utils.network import check_internet_connection
from kode_arrow.ui.dialogs import UIWindowManager

class LicensingService:
    def __init__(self, firebase_service):
        self.firebase = firebase_service

    def validate_and_activate(self, email, hardware_id, premium_file_path, is_research=False):
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
        if not check_internet_connection():
            messagebox.showinfo("Error", "Please check your internet connection again.")
            return False

        if email.strip().lower() == "freeforever@kodearrow.dev":
            collection = "ControlGroup"
        else:
            collection = "ControlGroup" if is_research else "users"
        user_ref = self.firebase.db.collection(collection).document(email)
        user_doc = user_ref.get()

        if user_doc.exists:
            devices_ref = user_ref.collection('devices')
            devices_query = devices_ref.get()
            
            exp_date_str = user_doc.get('expiration_date')
            if exp_date_str:
                expiration_date = datetime.strptime(exp_date_str, '%Y-%m-%d')
                if datetime.today() >= expiration_date:
                    UIWindowManager.showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us  and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
                    return False

            hardware_exists = False
            for device in devices_query:
                dev_id = device.to_dict().get('id')
                if dev_id == hardware_id or dev_id == "TrailVersion":
                    hardware_exists = True
                    break

            if hardware_exists:
                content += f"\n\nEmail: {email}\n"
                create_hidden_file(premium_file_path, content)
                return True
            elif email.strip().lower() != "freeforever@kodearrow.dev" and len(devices_query) >= (1 if is_research else 4):
                messagebox.showinfo("Error", "Maximum devices reached")
                return False
            else:
                device_data = {'id': hardware_id}
                devices_ref.document(f'device{len(devices_query) + 1}').set(device_data)
                content += f"\n\nEmail: {email}\n"
                create_hidden_file(premium_file_path, content)
                return True
        else:
            messagebox.showinfo("Registration not Found", "Registration not Found: Please check your email")
            return False

    def validate_email_info_on_startup(self, premium_file_path, find_email_fn, is_research=False):
        if os.path.exists(premium_file_path):
            email = find_email_fn(premium_file_path)
            if email:
                if email.strip().lower() == "freeforever@kodearrow.dev":
                    collection = "ControlGroup"
                else:
                    collection = "ControlGroup" if is_research else "users"
                user_ref = self.firebase.db.collection(collection).document(email)
                user_doc = user_ref.get()
                
                if user_doc.exists:
                    exp_date_str = user_doc.get('expiration_date')
                    if exp_date_str:
                        expiration_date = datetime.strptime(exp_date_str, '%Y-%m-%d')
                        if datetime.today() < expiration_date:
                            return True
                        else:
                            os.remove(premium_file_path)
                            UIWindowManager.showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us  and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
                    else:
                        os.remove(premium_file_path)
                        UIWindowManager.showMessage_subscriptionEnded("your Subscription Period has ended :(\nThank you for joining us  and hope you enjoyed it!\n\nPlase renew your subsription, and enjoy premium services again")
                else:
                    os.remove(premium_file_path)
                    UIWindowManager.showMessage_subscriptionEnded("A change in permission has been noticed\nPlease re-enter your email to activate premium version")
            else:
                os.remove(premium_file_path)
                UIWindowManager.showMessage_subscriptionEnded("A change in permission has been noticed\nPlease re-enter your email to activate premium version")
        return False
