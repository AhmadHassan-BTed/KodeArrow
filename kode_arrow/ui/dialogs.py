import webbrowser
from tkinter import BOTH, messagebox
from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel, CTkEntry
import customtkinter as ctk
import os
from kode_arrow.security.encryption import encrypt_hardware_id
from kode_arrow.security.hardware_identifier import get_hardware_id
from plyer import notification

class UIWindowManager:
    windows = []

    @staticmethod
    def show_notification():
        notification.notify(
            title='KodeArrow in system tray',
            message='Right-Click KodeArrow icon to open',
            app_name='KodeArrow',
            timeout=0,
            app_icon=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico'))
        )

    @staticmethod
    def showMessage_subscriptionEnded(message):
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico')))
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        ctk.set_appearance_mode("Light")
        app.resizable(False, False)

        def closeWindow_andBuySubscription():
            webbrowser.open("kodearrow.wuaze.com/payment.html")
            app.after(150, app.destroy)

        frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
        title = CTkLabel(master=frame1, text="KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
        subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
        labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 13))
        btn = CTkButton(master=frame1, text="Renew Subscription", width=180, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow_andBuySubscription)

        frame1.pack(fill=BOTH, expand=True)
        title.place(relx=0.5, rely=0.1, anchor="center")
        subtitle.place(relx=0.5, rely=0.2, anchor="center")

        w, h = 450, 250
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
        labelLocked.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.80, anchor="center")
        app.mainloop()

    @staticmethod
    def showMessage_versionEnded(message):
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico')))
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        ctk.set_appearance_mode("Light")
        app.resizable(False, False)

        def closeWindow_andBuySubscription():
            webbrowser.open("kodearrow.wuaze.com/")
            app.after(150, app.destroy)

        frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
        title = CTkLabel(master=frame1, text="KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
        subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
        labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 13))
        btn = CTkButton(master=frame1, text="Download New Version", width=180, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow_andBuySubscription)

        frame1.pack(fill=BOTH, expand=True)
        title.place(relx=0.5, rely=0.1, anchor="center")
        subtitle.place(relx=0.5, rely=0.2, anchor="center")

        w, h = 450, 250
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
        labelLocked.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.80, anchor="center")
        app.mainloop()

    @staticmethod
    def show_instructions(is_premium):
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico')))
        UIWindowManager.windows.append(app)
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()

        ctk.set_appearance_mode("Light")
        app.resizable(False, False)

        def closeWindow():
            UIWindowManager.show_notification()
            app.after(150, app.destroy)

        def changeMessage():
            if is_premium:
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
        btnShowMore = CTkButton(master=frame1, text="➜", width=30, height=15, corner_radius=1, fg_color="white",text_color="#00207f", hover_color="white", bg_color="white", command=changeMessage, font=("Arial", 24))
        showLock = ctk.CTkLabel( master=frame1, text="🔒", bg_color="transparent", text_color="#00207f", font=("Bahnschrif", 50, "bold"))
        padlockText = ctk.CTkLabel( master=frame1, text="These services are premium locked", bg_color="transparent", text_color="black", font=("Bahnschrif", 12, "bold"))

        frame1.pack(fill=BOTH, expand=True)
        title.place(relx=0.5, rely=0.1, anchor="center")
        subtitle.place(relx=0.5, rely=0.164, anchor="center")

        if is_premium:
            w, h = 480, 350
            app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
            labelUnlocked.place(relx=0.5, rely=0.5, anchor="center")
            btn.place(relx=0.5, rely=0.87, anchor="center")
            btnShowMore.place(relx=0.9, rely=0.87, anchor="center")
        else:
            w, h = 480, 360
            app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
            labelLocked.place(relx=0.5, rely=0.51, anchor="center")
            btn.place(relx=0.5, rely=0.88, anchor="center")
            btnShowMore.place(relx=0.9, rely=0.88, anchor="center")

        app.mainloop()

    @staticmethod
    def showMessage_success(title_text, message):
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico')))
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        ctk.set_appearance_mode("Light")
        app.resizable(False, False)

        frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
        title = CTkLabel(master=frame1, text=title_text, bg_color="white", text_color="#00207f", font=("Bahnschrift", 22, "bold"))
        label = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 14))
        btn = CTkButton(master=frame1, text="Awesome!", width=120, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=lambda: app.after(150, app.destroy))

        frame1.pack(fill=BOTH, expand=True)
        title.place(relx=0.5, rely=0.25, anchor="center")
        label.place(relx=0.5, rely=0.55, anchor="center")
        btn.place(relx=0.5, rely=0.82, anchor="center")

        w, h = 400, 200
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
        app.mainloop()

    @staticmethod
    def unlock_functionality(on_submit):
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico')))
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()

        w, h = 450, 250
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
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
            email = field.get().strip().lower()
            if not email:
                messagebox.showwarning("Warning", "Please enter an email address.")
                return
            if on_submit(email):
                app.after(150, app.destroy)
                UIWindowManager.showMessage_success("Congratulations!", "Premium Unlocked Successfully.\n\nEnjoy all KodeArrow features!")

    
        btn = CTkButton(master=frame1, text="Submit", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#000d34", bg_color="white", command=submit_key)
        btn.place(relx=0.5, rely=0.79, anchor="center")
        app.mainloop()

    @staticmethod
    def close_windows():
        for window in UIWindowManager.windows[:]:
            if window.winfo_exists():
                window.destroy()
                UIWindowManager.windows.remove(window)
