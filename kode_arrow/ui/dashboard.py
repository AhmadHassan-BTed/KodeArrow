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

        w, h = 850, 550
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))

        # ------------------------------------------------
        # THEME CONSTANTS (Strictly matching dialogs.py)
        # ------------------------------------------------
        PRIMARY_COLOR = "#00207f"    # The exact royal blue from dialogs.py
        PRIMARY_HOVER = "#00134c"    # The exact hover blue from dialogs.py
        BG_WHITE = "white"           # The exact background color from dialogs.py
        TEXT_BLACK = "black"         # The exact text color from dialogs.py
        
        FONT_FAMILY = "Bahnschrift"  # The exact font from dialogs.py
        CORNER_RADIUS = 7            # The exact button corner radius from dialogs.py
        
        # Main Container
        container = CTkFrame(master=app, fg_color=BG_WHITE, corner_radius=0)
        container.pack(fill=BOTH, expand=True)

        # ------------------------------------------------
        # FULL HEIGHT SIDEBAR (Using Primary Color)
        # ------------------------------------------------
        sidebar = CTkFrame(master=container, width=240, fg_color=PRIMARY_COLOR, corner_radius=0)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        # ------------------------------------------------
        # MAIN CONTENT AREA (Pure White)
        # ------------------------------------------------
        main_content = CTkFrame(master=container, fg_color=BG_WHITE, corner_radius=0)
        main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=45, pady=40)

        home_frame = CTkFrame(master=main_content, fg_color=BG_WHITE)
        settings_frame = CTkFrame(master=main_content, fg_color=BG_WHITE)

        btn_nav_home = None
        btn_nav_settings = None

        def update_nav_styles(active_tab):
            active_color = PRIMARY_HOVER
            default_color = "transparent"

            btn_nav_home.configure(fg_color=active_color if active_tab == "home" else default_color)
            btn_nav_settings.configure(fg_color=active_color if active_tab == "settings" else default_color)

        def show_home():
            settings_frame.pack_forget()
            home_frame.pack(fill=BOTH, expand=True)
            update_nav_styles("home")

        def show_settings():
            home_frame.pack_forget()
            settings_frame.pack(fill=BOTH, expand=True)
            update_nav_styles("settings")

        # Sidebar Branding
        logo_label = CTkLabel(master=sidebar, text="KodeArrow© 2023", font=(FONT_FAMILY, 20, "bold"), text_color="white")
        logo_label.pack(pady=(45, 10), padx=25, anchor="w")
        subtitle_label = CTkLabel(master=sidebar, text="a project by Ahmad Hassan", font=(FONT_FAMILY, 12, "bold"), text_color="white")
        subtitle_label.pack(pady=(0, 40), padx=25, anchor="w")

        # Sidebar Navigation Buttons
        nav_container = CTkFrame(master=sidebar, fg_color="transparent")
        nav_container.pack(fill=X, padx=15)

        btn_nav_home = CTkButton(master=nav_container, text="Dashboard", font=(FONT_FAMILY, 15), height=40, corner_radius=CORNER_RADIUS,
                                 fg_color="transparent", text_color="white", hover_color=PRIMARY_HOVER, anchor="w", command=show_home)
        btn_nav_home.pack(fill=X, pady=4)
        
        btn_nav_settings = CTkButton(master=nav_container, text="Shortcuts", font=(FONT_FAMILY, 15), height=40, corner_radius=CORNER_RADIUS,
                                     fg_color="transparent", text_color="white", hover_color=PRIMARY_HOVER, anchor="w", command=show_settings)
        btn_nav_settings.pack(fill=X, pady=4)

        # Bottom Footer in Sidebar
        footer_frame = CTkFrame(master=sidebar, fg_color="transparent")
        footer_frame.pack(side=BOTTOM, fill=X, pady=30, padx=15)

        btn_website = CTkButton(master=footer_frame, text="Visit Website", height=35, corner_radius=CORNER_RADIUS, font=(FONT_FAMILY, 14),
                                fg_color="white", text_color=PRIMARY_COLOR, hover_color="#e6e6e6", command=on_open_website)
        btn_website.pack(fill=X, pady=(0, 10))

        def close_and_exit():
            app.destroy()
            on_exit()

        btn_exit = CTkButton(master=footer_frame, text="Exit Application", height=35, corner_radius=CORNER_RADIUS, font=(FONT_FAMILY, 14),
                             fg_color="transparent", text_color="#FFB3B3", border_width=1, border_color="#FFB3B3", hover_color="#cc0000", command=close_and_exit)
        btn_exit.pack(fill=X)

        # ==========================================
        # HOME TAB
        # ==========================================
        CTkLabel(master=home_frame, text="Overview", font=(FONT_FAMILY, 28, "bold"), text_color=PRIMARY_COLOR).pack(anchor="w", pady=(0, 30))

        is_premium = is_premium_fn()
        status_text = "Premium Active" if is_premium else "Unlicensed Mode"
        status_color = "#008000" if is_premium else "#cc0000" 
        
        # Status Section (No cards, flat design like dialogs.py)
        CTkLabel(master=home_frame, text="License Status:", font=(FONT_FAMILY, 16, "bold"), text_color=TEXT_BLACK).pack(anchor="w", pady=(0, 5))
        CTkLabel(master=home_frame, text=status_text, font=(FONT_FAMILY, 24, "bold"), text_color=status_color).pack(anchor="w", pady=(0, 30))

        # Auto-Start Section
        CTkLabel(master=home_frame, text="System Startup:", font=(FONT_FAMILY, 16, "bold"), text_color=TEXT_BLACK).pack(anchor="w", pady=(0, 5))
        CTkLabel(master=home_frame, text="Launch KodeArrow in the background when Windows starts", font=(FONT_FAMILY, 14), text_color=TEXT_BLACK).pack(anchor="w", pady=(0, 10))

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        
        switch = CTkSwitch(master=home_frame, text=" Enable Auto-Start", command=toggle_autostart, variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#cccccc", progress_color=PRIMARY_COLOR, text_color=TEXT_BLACK, font=(FONT_FAMILY, 14, "bold"))
        switch.pack(anchor="w", pady=10)

        # ==========================================
        # SETTINGS TAB
        # ==========================================
        CTkLabel(master=settings_frame, text="Shortcuts", font=(FONT_FAMILY, 28, "bold"), text_color=PRIMARY_COLOR).pack(anchor="w", pady=(0, 10))
        CTkLabel(master=settings_frame, text="Modify your personal workflow keys. Hold 'Alt' to trigger.", font=(FONT_FAMILY, 14), text_color=TEXT_BLACK).pack(anchor="w", pady=(0, 30))

        grid_frame = CTkFrame(master=settings_frame, fg_color="transparent")
        grid_frame.pack(fill=BOTH, expand=True)

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        
        entries = {}
        row, col = 0, 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_frame, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=(0, 50), pady=15, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}:", font=(FONT_FAMILY, 15, "bold"), width=80, anchor="w", text_color=TEXT_BLACK).pack(side=LEFT)
            
            entry = CTkEntry(master=field_frame, width=45, height=35, font=(FONT_FAMILY, 15), justify="center", 
                             fg_color="#f2f2f2", text_color=TEXT_BLACK, border_width=1, border_color="#cccccc", corner_radius=CORNER_RADIUS)
            entry.insert(0, current_key)
            entry.pack(side=LEFT, padx=10)
            entries[action] = entry
            
            col += 1
            if col > 1:
                col, row = 0, row + 1

        def save_hotkeys():
            new_prefs = prefs.copy()
            for action, entry in entries.items():
                val = entry.get().strip().lower()
                if len(val) == 1: new_prefs["hotkeys"][action] = val
            UserPrefs.save(new_prefs)
            on_reload_engine() 
            
            save_btn.configure(text="Changes Saved")
            app.after(2500, lambda: save_btn.configure(text="Save Preferences"))

        save_btn = CTkButton(master=settings_frame, text="Save Preferences", width=160, height=40, corner_radius=CORNER_RADIUS, font=(FONT_FAMILY, 14), 
                             fg_color=PRIMARY_COLOR, text_color="white", hover_color=PRIMARY_HOVER, command=save_hotkeys)
        save_btn.pack(anchor="w", pady=(30, 0))

        show_home()
        app.mainloop()
