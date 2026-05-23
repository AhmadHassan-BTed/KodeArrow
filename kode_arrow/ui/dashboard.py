import os
from customtkinter import (CTk, CTkFrame, CTkLabel, CTkButton, CTkSwitch, CTkEntry,
                         BOTH, LEFT, RIGHT, TOP, BOTTOM, X, Y, StringVar, set_appearance_mode)
from kode_arrow.utils.resource import get_resource_path
from kode_arrow.utils.system import enable_autostart, disable_autostart, is_autostart_enabled
from kode_arrow.config.user_prefs import UserPrefs

class DashboardWindow:
    @staticmethod
    def open(is_premium_fn, on_open_website, on_exit, on_reload_engine):
        app = CTk()
        app.title("KodeArrow Dashboard")
        app.iconbitmap(get_resource_path(os.path.join('assets', 'branding', 'icon.ico')))
        
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        set_appearance_mode("Light")
        app.resizable(False, False)

        w, h = 750, 500
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))

        # Define Colors
        BG_COLOR = "#f5f6fa"
        SIDEBAR_COLOR = "#ffffff"
        PRIMARY_BLUE = "#00207f"
        HOVER_BLUE = "#00134c"

        # Container
        container = CTkFrame(master=app, fg_color=BG_COLOR)
        container.pack(fill=BOTH, expand=True)

        # Sidebar
        sidebar = CTkFrame(master=container, width=200, fg_color=SIDEBAR_COLOR, corner_radius=0)
        sidebar.pack(side=LEFT, fill=Y)

        # Main Content Area
        main_content = CTkFrame(master=container, fg_color=BG_COLOR, corner_radius=0)
        main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=30, pady=30)

        # Pages
        home_frame = CTkFrame(master=main_content, fg_color="transparent")
        settings_frame = CTkFrame(master=main_content, fg_color="transparent")

        def show_home():
            settings_frame.pack_forget()
            home_frame.pack(fill=BOTH, expand=True)

        def show_settings():
            home_frame.pack_forget()
            settings_frame.pack(fill=BOTH, expand=True)

        # Sidebar Branding
        logo_label = CTkLabel(master=sidebar, text="KodeArrow", font=("Bahnschrift", 22, "bold"), text_color=PRIMARY_BLUE)
        logo_label.pack(pady=(40, 40))

        # Sidebar Navigation Buttons
        btn_nav_home = CTkButton(master=sidebar, text="Home", font=("Bahnschrift", 15), fg_color="transparent", text_color="black", hover_color="#e0e4f0", anchor="w", command=show_home)
        btn_nav_home.pack(fill=X, padx=10, pady=5)
        
        btn_nav_settings = CTkButton(master=sidebar, text="Hotkeys", font=("Bahnschrift", 15), fg_color="transparent", text_color="black", hover_color="#e0e4f0", anchor="w", command=show_settings)
        btn_nav_settings.pack(fill=X, padx=10, pady=5)

        # ==========================================
        # HOME TAB
        # ==========================================
        title = CTkLabel(master=home_frame, text="Overview", font=("Bahnschrift", 26, "bold"), text_color="black")
        title.pack(anchor="w", pady=(0, 20))

        is_premium = is_premium_fn()
        status_text = "Premium Unlocked" if is_premium else "Unlicensed / Free"
        status_color = "#008000" if is_premium else "#d90000"
        
        status_box = CTkFrame(master=home_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
        status_box.pack(fill=X, pady=(0, 20), ipadx=15, ipady=15)
        
        CTkLabel(master=status_box, text="Current Status", font=("Bahnschrift", 14), text_color="gray").pack(anchor="w", padx=15, pady=(10, 0))
        CTkLabel(master=status_box, text=status_text, font=("Bahnschrift", 20, "bold"), text_color=status_color).pack(anchor="w", padx=15, pady=(0, 10))

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        switch = CTkSwitch(master=home_frame, text=" Start KodeArrow silently with Windows", command=toggle_autostart,
                           variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#cccccc", progress_color=PRIMARY_BLUE, text_color="black", font=("Bahnschrift", 14))
        switch.pack(anchor="w", pady=10)

        # ==========================================
        # SETTINGS TAB
        # ==========================================
        CTkLabel(master=settings_frame, text="Hotkey Configuration", font=("Bahnschrift", 26, "bold"), text_color="black").pack(anchor="w", pady=(0, 10))
        CTkLabel(master=settings_frame, text="All shortcuts are triggered holding the 'Alt' modifier key.", font=("Bahnschrift", 13), text_color="gray").pack(anchor="w", pady=(0, 20))

        grid_frame = CTkFrame(master=settings_frame, fg_color="transparent")
        grid_frame.pack(fill=BOTH, expand=True)

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        
        entries = {}
        row = 0
        col = 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_frame, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=(0, 40), pady=12, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}:", font=("Bahnschrift", 14), width=80, anchor="w", text_color="black").pack(side=LEFT)
            entry = CTkEntry(master=field_frame, width=50, font=("Bahnschrift", 14), justify="center", fg_color="white", text_color="black", border_color="#cccccc")
            entry.insert(0, current_key)
            entry.pack(side=LEFT, padx=10)
            entries[action] = entry
            
            col += 1
            if col > 1:
                col = 0
                row += 1

        def save_hotkeys():
            new_prefs = prefs.copy()
            for action, entry in entries.items():
                val = entry.get().strip().lower()
                if len(val) == 1: 
                    new_prefs["hotkeys"][action] = val
            UserPrefs.save(new_prefs)
            on_reload_engine() 
            
            save_btn.configure(text="Saved!")
            app.after(2000, lambda: save_btn.configure(text="Apply Shortcuts"))

        save_btn = CTkButton(master=settings_frame, text="Apply Shortcuts", width=150, height=35, corner_radius=7, fg_color=PRIMARY_BLUE, hover_color=HOVER_BLUE, command=save_hotkeys)
        save_btn.pack(anchor="e", pady=20)

        # ==========================================
        # BOTTOM FOOTER (Global to sidebar)
        # ==========================================
        footer_frame = CTkFrame(master=sidebar, fg_color="transparent")
        footer_frame.pack(side=BOTTOM, fill=X, pady=30, padx=15)

        btn_website = CTkButton(master=footer_frame, text="Visit Website", height=32, corner_radius=6, 
                                fg_color="white", text_color=PRIMARY_BLUE, hover_color="#f0f0f0",
                                border_width=1.5, border_color=PRIMARY_BLUE, command=on_open_website)
        btn_website.pack(fill=X, pady=(0, 10))

        def close_and_exit():
            app.destroy()
            on_exit()

        btn_exit = CTkButton(master=footer_frame, text="Exit App", height=32, corner_radius=6, 
                             fg_color="white", text_color="#d90000", hover_color="#fff0f0",
                             border_width=1.5, border_color="#d90000", command=close_and_exit)
        btn_exit.pack(fill=X)

        # Start on Home
        show_home()
        app.mainloop()
