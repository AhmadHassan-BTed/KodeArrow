from customtkinter import *
import customtkinter as ctk

def is_premium():
    return 0


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
        "Thank you for using KodeArrow, a project of ByTed Technologies\n\n\n"
        "Alt + I\n(Arrow Up)\n\n"
        "Alt + J\t\t\t\tAlt + L\n(Arrow 🔒 Left)\t\t\t(Arrow 🔒 Right)\n\n"
        "Alt + K\n(Arrow Down)\n\n\n"
        "Note: Please buy Premium version to unlock locked keys"
    )

    messageUnlocked = (
        "Thank you for using KodeArrow, a project of ByTed Technologies\n\n\n"
        "Alt + I\n(Arrow Up)\n\n"
        "Alt + J\t\t\t\tAlt + L\n(Arrow Left)\t\t\t(Arrow Right)\n\n"
        "Alt + K\n(Arrow Down)\n\n\n"
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

        labelUnlocked.place(relx=0.5, rely=0.55, anchor="center")
        btn.place(relx=0.5, rely=0.85, anchor="center")
    else:
        w = 450
        h = 360
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        labelLocked.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.88, anchor="center")

    app.mainloop()

def EnterEmail():
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

    def submitEmail():
        entered_email = field.get()
        print("entered email is: ", entered_email)
        app.destroy()

    message = (
        "Please enter your Email"
    )

    frame1 = CTkFrame(master=app, bg_color="white", fg_color="white")
    title = CTkLabel(master=frame1, text="Welcome to KodeArrow© 2023", bg_color="white", text_color="#00207f", font=("Bahnschrift", 20, "bold"))
    subtitle = CTkLabel(master=frame1, text="a project by Ahmad Hassan", bg_color="white", text_color="#00207f", font=("Bahnschrift", 16, "bold"))
    label = CTkLabel(master=frame1, text=message, bg_color="white", text_color="black", font=("Bahnschrift", 14))
    field = CTkEntry(master=frame1, placeholder_text="Email", width=350, height=40)
    btn = CTkButton(master=frame1, text="Submit", width=90, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=submitEmail)

    frame1.pack(fill=BOTH, expand=True)
    title.place(relx=0.5, rely=0.1, anchor="center")
    subtitle.place(relx=0.5, rely=0.2, anchor="center")
    label.place(relx=0.289, rely=0.4, anchor="center")
    field.place(relx=0.5, rely=0.55, anchor="center")
    btn.place(relx=0.5, rely=0.79, anchor="center")
    app.mainloop()

showMessage()
EnterEmail()