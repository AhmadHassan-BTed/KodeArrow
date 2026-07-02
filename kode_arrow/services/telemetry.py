import threading
import logging
from kode_arrow.utils.file import read_from_file, add_hidden_attribute, remove_hidden_attribute, find_email_in_file

logger = logging.getLogger("KodeArrow.Telemetry")


class TelemetryService:
    def __init__(self, firebase_service, premium_file_path, usage_file_path="premium_Key_metadata.txt"):
        self.firebase = firebase_service
        self.premium_file_path = premium_file_path
        self.usage_file = usage_file_path

    def run_async_upload_threaded(self):
        def target_function():
            try:
                remove_hidden_attribute(self.usage_file)
                temp_total_keyStrokes, temp_total_shortcuts, temp_total_runtime = read_from_file(self.usage_file)

                email = find_email_in_file(self.premium_file_path)
                if not email: return
                
                doc_ref_user = self.firebase.db.collection('ControlGroup').document(email)
                usage_ref = doc_ref_user.collection('usage').document('usage_data')

                usage_doc = usage_ref.get()
                if usage_doc.exists:
                    existing_data = usage_doc.to_dict()
                    existing_data['charactersTyped'] += temp_total_keyStrokes
                    existing_data['kodeArrowHotkeys'] += temp_total_shortcuts
                    existing_data['TotalUsageMinutes'] += temp_total_runtime
                    
                    usage_ref.set(existing_data)
                    
                    with open(self.usage_file, "w") as file:
                        file.write(f"{0}\n{0}\n{0}\n")
                
                add_hidden_attribute(self.usage_file)
            except Exception:
                pass  # Non-critical telemetry — silently ignore

        thread = threading.Thread(target=target_function, daemon=True)
        thread.start()
        return thread
