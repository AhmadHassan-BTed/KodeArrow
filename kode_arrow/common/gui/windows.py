import webbrowser
from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
import threading
from ..config.settings import Config

class UIWindowManager:
    """Manages the complex CustomTkinter windows of KodeArrow."""
    
    @staticmethod
    def show_email_input_dialog(on_submit_callback=None):
        """Shows a responsive email input dialog for unlocking premium access.
        
        Args:
            on_submit_callback: Optional callback function that receives the email address
        """
        app = CTk()
        app.title(Config.APP_NAME)
        app.resizable(False, False)
        
        # Get screen dimensions
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        w = 450
        h = 250
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        app.geometry(f'{w}x{h}+{x}+{y}')
        
        ctk.set_appearance_mode("Light")
        
        # Create main frame
        frame = CTkFrame(master=app, bg_color="white", fg_color="white")
        frame.pack(fill=BOTH, expand=True)
        
        # Add title and subtitle
        title = CTkLabel(master=frame, text="Unlock Premium", bg_color="white", 
                        text_color="#00207f", font=("Bahnschrift", 20, "bold"))
        subtitle = CTkLabel(master=frame, text="Enter your registered email", 
                           bg_color="white", text_color="#00207f", font=("Bahnschrift", 12))
        
        # Add email entry field
        email_field = CTkEntry(master=frame, placeholder_text="your.email@example.com", 
                              width=350, height=40, font=("Bahnschrift", 12))
        
        def submit_email():
            email = email_field.get().strip()
            if email:
                if on_submit_callback:
                    on_submit_callback(email)
                app.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid email address")
        
        def close_window():
            app.destroy()
        
        # Add buttons
        submit_btn = CTkButton(master=frame, text="Unlock", width=90, height=35, 
                              corner_radius=7, fg_color="#00207f", 
                              hover_color="#00134c", bg_color="white", command=submit_email)
        cancel_btn = CTkButton(master=frame, text="Cancel", width=90, height=35, 
                              corner_radius=7, fg_color="#c0c0c0", 
                              hover_color="#808080", bg_color="white", command=close_window)
        
        # Position widgets
        title.place(relx=0.5, rely=0.15, anchor="center")
        subtitle.place(relx=0.5, rely=0.35, anchor="center")
        email_field.place(relx=0.5, rely=0.55, anchor="center")
        submit_btn.place(relx=0.35, rely=0.80, anchor="center")
        cancel_btn.place(relx=0.65, rely=0.80, anchor="center")
        
        # Allow Enter key to submit
        email_field.bind("<Return>", lambda e: submit_email())
        
        # Allow Escape key to cancel
        app.bind("<Escape>", lambda e: close_window())
        
        # Focus on email field
        email_field.focus()
        
        app.mainloop()
    
    @staticmethod
    def show_subscription_ended(message, renew_url="https://kodearrow.wuaze.com/payment.html"):
        app = CTk()
        app.title(Config.APP_NAME)
        # Note: Icon path resolution would happen here
        ctk.set_appearance_mode("Light")
        app.resizable(False, False)

        def on_renew():
            webbrowser.open(renew_url)
            app.destroy()

        frame = CTkFrame(master=app, bg_color="white", fg_color="white")
        title = CTkLabel(master=frame, text="KodeArrow© 2023", font=("Bahnschrift", 20, "bold"))
        msg_label = CTkLabel(master=frame, text=message, font=("Bahnschrift", 13))
        btn = CTkButton(master=frame, text="Renew Subscription", command=on_renew)
        
        frame.pack(fill=BOTH, expand=True)
        title.place(relx=0.5, rely=0.1, anchor="center")
        msg_label.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.80, anchor="center")
        app.mainloop()

    @staticmethod
    def show_instructions(is_premium=False):
        app = CTk()
        app.title(Config.APP_NAME)
        
        msg = (
            "Thank you for using KodeArrow, a product of ByTed Technologies\n\n"
            "Alt + I\n(Arrow Up)\n\n"
            "Alt + J\t\t\t\tAlt + L\n(Arrow Left)\t\t\t(Arrow Right)\n\n"
            "Alt + K\n(Arrow Down)\n\n\"Right click KodeArrow icon in System Tray to access menu\""
        ) if is_premium else (
            "Thank you for using KodeArrow, a product of ByTed Technologies\n\n"
            "Alt + I\n(Arrow 🔒 Up)\n\n"
            "Alt + J\t\t\t\tAlt + L\n(Arrow Left)\t\t\t(Arrow Right)\n\n"
            "Alt + K\n(Arrow 🔒 Down)\n\n"
            "\"Right click KodeArrow icon in System Tray to access menu\"\nNote: Please buy Premium version to unlock locked keys"
        )
        
        messagebox.showinfo("Welcome to KodeArrow", msg)
        app.destroy()

    @staticmethod
    def show_version_ended(message):
        app = CTk()
        app.title("KodeArrow")
        ctk.set_appearance_mode("Light")
        
        def on_download():
            webbrowser.open("https://kodearrow.wuaze.com/")
            app.destroy()

        frame = CTkFrame(master=app, bg_color="white", fg_color="white")
        label = CTkLabel(master=frame, text=message, font=("Bahnschrift", 13))
        btn = CTkButton(master=frame, text="Download New Version", command=on_download)
        
        frame.pack(fill=BOTH, expand=True)
        label.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.80, anchor="center")
        app.mainloop()
