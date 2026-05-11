import webbrowser
from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
from ..config.settings import Config

class UIWindowManager:
    """Manages the complex CustomTkinter windows of KodeArrow."""
    
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
