# from customtkinter import *
# import customtkinter as ctk

# def is_premium():
#     return 0


# def showMessage():
#     app = CTk()
#     app.title("KodeArrow")
#     app.iconbitmap("icon.ico")

#     ws = app.winfo_screenwidth()
#     hs = app.winfo_screenheight()

#     ctk.set_appearance_mode("Light")
#     app.resizable(False, False)

#     def closeWindow():
#         app.destroy()

#     message = (
#         "Thank you for using KodeArrow, a project of ByTed Technologies\n\n\n"
#         "Alt + I\n(Arrow Up)\n\n"
#         "Alt + J\t\t\t\tAlt + L\n(Arrow 🔒 Left)\t\t\t(Arrow 🔒 Right)\n\n"
#         "Alt + K\n(Arrow Down)\n\n\n"
#         "Note: Please buy Premium version to unlock locked keys"
#     )

#     messageUnlocked = (
#         "Thank you for using KodeArrow, a project of ByTed Technologies\n\n\n"
#         "Alt + I\n(Arrow Up)\n\n"
#         "Alt + J\t\t\t\tAlt + L\n(Arrow Left)\t\t\t(Arrow Right)\n\n"
#         "Alt + K\n(Arrow Down)\n\n\n"
#     )

#     frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
#     title = CTkLabel(master=frame1, text="Welcome to KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
#     subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
#     labelLocked = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 12))
#     labelUnlocked = CTkLabel(master=frame1, text=messageUnlocked, bg_color="white", text_color="black", font=("Bahnschrift", 12))
#     btn = CTkButton(master=frame1, text="Ok", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=closeWindow)

#     frame1.pack(fill=BOTH, expand=True)
#     title.place(relx=0.5, rely=0.1, anchor="center")
#     subtitle.place(relx=0.5, rely=0.164, anchor="center")

#     if is_premium():
#         w = 450
#         h = 340
#         x = (ws/2) - (w/2)
#         y = (hs/2) - (h/2)
#         app.geometry('%dx%d+%d+%d' % (w, h, x, y))

#         labelUnlocked.place(relx=0.5, rely=0.55, anchor="center")
#         btn.place(relx=0.5, rely=0.85, anchor="center")
#     else:
#         w = 450
#         h = 360
#         x = (ws/2) - (w/2)
#         y = (hs/2) - (h/2)
#         app.geometry('%dx%d+%d+%d' % (w, h, x, y))

#         labelLocked.place(relx=0.5, rely=0.5, anchor="center")
#         btn.place(relx=0.5, rely=0.88, anchor="center")

#     app.mainloop()

# def EnterEmail():
#     app = CTk()

#     app.title("KodeArrow")
#     app.iconbitmap("icon.ico")

#     ws = app.winfo_screenwidth()
#     hs = app.winfo_screenheight()

#     w = 450
#     h = 250
#     x = (ws/2) - (w/2)
#     y = (hs/2) - (h/2)
#     app.geometry('%dx%d+%d+%d' % (w, h, x, y))

#     ctk.set_appearance_mode("Light")
#     app.resizable(False, False)

#     def submitEmail():
#         entered_email = field.get()
#         print("entered email is: ", entered_email)
#         app.destroy()

#     message = (
#         "Please enter your Email"
#     )

#     frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
#     title = CTkLabel(master=frame1, text="Welcome to KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
#     subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
#     label = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 14))
#     field = CTkEntry(master=frame1, placeholder_text="Email", width=350, height=40)
#     btn = CTkButton(master=frame1, text="Submit", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=submitEmail)

#     frame1.pack(fill=BOTH, expand=True)
#     title.place(relx=0.5, rely=0.1, anchor="center")
#     subtitle.place(relx=0.5, rely=0.2, anchor="center")
#     label.place(relx=0.289, rely=0.4, anchor="center")
#     field.place(relx=0.5, rely=0.55, anchor="center")
#     btn.place(relx=0.5, rely=0.79, anchor="center")
#     app.mainloop()

# showMessage()
# EnterEmail()

def is_premium():
    return False

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

    def changeMessage():
        # app.destroy()
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

        # if showMore:
        #     showMore.destroy()
        #     labelUnlocked.place(relx=0.5, rely=0.5, anchor="center")



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

    showMoreMessage = (
        " Thank you for using KodeArrow, a product of ByTed Technologies\n\n\n"
        "{:<30} {:<30} {:<29} {:<1}\n"
        "{:23} {:<30} {:<26} {:<0}\n\n\n\n"
        "{:<30} {:<30} {:<29} {:<1}\n"
        "{:<23} {:<22} {:<22} {:<0}\n"
    ).format(
            "Alt + U", "Alt + I", "Alt + O", "Alt + P",
            "(Home)", "(Arrow Up)", "(End)", "(PageUp)",
            "Alt + J", "Alt + K", "Alt + L", "Alt + ;",
            "(Arrow Left)", "(Arrow Down)", "(Arrow Right)", "(PageDown)"
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
        w = 450
        h = 350
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))
        labelUnlocked.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.87, anchor="center")
        btnShowMore.place(relx=0.9, rely=0.87, anchor="center")
    else:
        w = 450
        h = 360
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        labelLocked.place(relx=0.5, rely=0.51, anchor="center")
        btn.place(relx=0.5, rely=0.88, anchor="center")
        btnShowMore.place(relx=0.9, rely=0.88, anchor="center")

    app.mainloop()

# Show the initial instructions when the program starts
showMessage()
