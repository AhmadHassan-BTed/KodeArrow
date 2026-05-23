import os
import webbrowser
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSwitch, BOTH, StringVar, set_appearance_mode
from kode_arrow.utils.resource import get_resource_path
from kode_arrow.utils.system import enable_autostart, disable_autostart, is_autostart_enabled

class DashboardWindow:
    @staticmethod
    def open(is_premium_fn, on_open_website, on_exit):
        app = CTk()
        app.title("KodeArrow Dashboard")
        app.iconbitmap(get_resource_path(os.path.join('assets', 'branding', 'icon.ico')))
        
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        set_appearance_mode("Light")
        app.resizable(False, False)

        frame = CTkFrame(master=app, bg_color="white", fg_color="white")
        frame.pack(fill=BOTH, expand=True)

        title = CTkLabel(master=frame, text="KodeArrow Dashboard", bg_color="white", text_color="#00207f", font=("Bahnschrift", 24, "bold"))
        title.place(relx=0.5, rely=0.15, anchor="center")

        is_premium = is_premium_fn()
        status_text = "Premium Unlocked" if is_premium else "Unlicensed / Free"
        status_color = "#008000" if is_premium else "#d90000"
        
        status_label = CTkLabel(master=frame, text=status_text, bg_color="white", text_color=status_color, font=("Bahnschrift", 16, "bold"))
        status_label.place(relx=0.5, rely=0.3, anchor="center")

        def toggle_autostart():
            if switch_var.get() == "on":
                enable_autostart()
            else:
                disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        switch = CTkSwitch(master=frame, text="Start with Windows", command=toggle_autostart,
                           variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#cccccc", progress_color="#00207f", text_color="black", font=("Bahnschrift", 14))
        switch.place(relx=0.5, rely=0.5, anchor="center")

        btn_website = CTkButton(master=frame, text="Visit Website", width=180, height=35, corner_radius=7, fg_color="#00207f", hover_color="#00134c", bg_color="white", command=on_open_website)
        btn_website.place(relx=0.5, rely=0.7, anchor="center")
        
        def close_and_exit():
            app.destroy()
            on_exit()

        btn_exit = CTkButton(master=frame, text="Exit KodeArrow", width=180, height=35, corner_radius=7, fg_color="#d90000", hover_color="#a60000", bg_color="white", command=close_and_exit)
        btn_exit.place(relx=0.5, rely=0.85, anchor="center")

        w, h = 450, 350
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))
        app.mainloop()
