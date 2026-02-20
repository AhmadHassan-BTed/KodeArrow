from datetime import datetime
import os
from .firebase import FirebaseService
from kode_arrow.infrastructure.storage.file_utils import create_hidden_file
from kode_arrow.infrastructure.config.settings import Config

class SubscriptionService:
    """Handles logic for device registration and subscription validation."""

    def __init__(self):
        self.firebase = FirebaseService()

    def validate_and_activate(self, email, hardware_id, premium_file_path, is_research=False):
        collection = "ControlGroup" if is_research else "users"
        max_devices = 1 if is_research else 4

        doc = self.firebase.get_user_doc(collection, email)
        if not doc or not doc.exists:
            return False, "Registration not found"

        # Date validation
        sub_date_str = doc.get('subscription_date')
        if sub_date_str:
            sub_date = datetime.strptime(sub_date_str, '%Y-%m-%d')
            if datetime.today() >= sub_date:
                return False, "Subscription expired"

        # Device validation
        user_ref = self.firebase.db.collection(collection).document(email)
        devices = user_ref.collection('devices').get()

        hardware_exists = any(d.to_dict().get('id') == hardware_id for d in devices)

        if hardware_exists:
            self._create_premium_file(premium_file_path, email)
            return True, "Success"

        if len(devices) >= max_devices:
            return False, "Maximum devices reached"

        # Register new device
        self.firebase.update_user_device(collection, email, hardware_id)
        self._create_premium_file(premium_file_path, email)
        return True, "Success"

    def _create_premium_file(self, path, email):
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
        content += f"\n\nEmail: {email}\n"
        create_hidden_file(path, content)
