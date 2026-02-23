import webbrowser
from tkinter import BOTH
from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel
import customtkinter as ctk
from tkinter import messagebox
import threading
from kode_arrow.config.settings import Config

class DialogManager:
    """Manages the complex CustomTkinter dialog windows of KodeArrow."""

    @staticmethod
    def show_instructions(is_premium=False):
        app = CTk()
        app.title("KodeArrow")
        
        window_width = 800
        window_height = 400
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        app.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Light")
        frame = CTkFrame(master=app, bg_color="white", fg_color="white")
        
        main_label = CTkLabel(master=frame, text="KodeArrow is running in background", font=("Bahnschrift", 24))
        
        instructions_text = "Instructions:\n1. Open KodeArrow\n2. Minimize it\n3. Start using shortcuts:\n   - CapsLock + I -> Up\n   - CapsLock + K -> Down\n   - CapsLock + J -> Left\n   - CapsLock + L -> Right\n   - CapsLock + H -> Delete\n   - CapsLock + U -> Backspace"
        if is_premium:
            instructions_text += "\n\nPremium features UNLOCKED:\n   - Alt + U -> Home\n   - Alt + O -> End\n   - Alt + P -> Delete\n   - Alt + ; -> Backspace\n   - Alt + [ -> PageUp\n   - Alt + ' -> PageDown"

        instructions = CTkLabel(master=frame, text=instructions_text, font=("Bahnschrift", 16), justify="left")

        def open_website():
            webbrowser.open("https://kodearrow.wuaze.com/")
            
        def on_ok():
            app.destroy()

        btn_ok = CTkButton(master=frame, text="OK", command=on_ok, width=120)
        btn_web = CTkButton(master=frame, text="Visit Website", command=open_website, width=120)

        frame.pack(fill=BOTH, expand=True)
        main_label.place(relx=0.5, rely=0.1, anchor="center")
        instructions.place(relx=0.5, rely=0.4, anchor="center")
        btn_ok.place(relx=0.4, rely=0.85, anchor="center")
        btn_web.place(relx=0.6, rely=0.85, anchor="center")

        app.mainloop()

class UIWindowManager:
    """Facade for startup UI flows."""
    @staticmethod
    def show_instructions(is_premium=False):
        DialogManager.show_instructions(is_premium=is_premium)
