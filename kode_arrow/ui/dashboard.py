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
        # THEME CONSTANTS (Inspired by the attached designs)
        # ------------------------------------------------
        SIDEBAR_BG = "#3A72FF"       # Vibrant solid blue from the inspiration
        SIDEBAR_HOVER = "#2A5CE6"    # Darker blue for sidebar button hover
        MAIN_BG = "#F8F9FB"          # Ultra-light gray for the main area
        CARD_BG = "#FFFFFF"          # Pure white for cards
        
        TEXT_DARK = "#1E1E24"        # Modern off-black
        TEXT_MUTED = "#8A8D93"       # Soft gray
        BORDER_LIGHT = "#E8EAEF"     # Extremely subtle borders for cards

        FONT_FAMILY = "Bahnschrift"
        
        # Main Container
        container = CTkFrame(master=app, fg_color=MAIN_BG, corner_radius=0)
        container.pack(fill=BOTH, expand=True)

        # ------------------------------------------------
        # FULL HEIGHT BLUE SIDEBAR
        # ------------------------------------------------
        sidebar = CTkFrame(master=container, width=240, fg_color=SIDEBAR_BG, corner_radius=0)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        # ------------------------------------------------
        # MAIN CONTENT AREA
        # ------------------------------------------------
        main_content = CTkFrame(master=container, fg_color="transparent")
        main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=45, pady=40)

        home_frame = CTkFrame(master=main_content, fg_color="transparent")
        settings_frame = CTkFrame(master=main_content, fg_color="transparent")

        btn_nav_home = None
        btn_nav_settings = None

        def update_nav_styles(active_tab):
            # Active tabs get a semi-transparent white highlight
            active_color = "#5588FF"
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
        logo_label = CTkLabel(master=sidebar, text="KodeArrow", font=(FONT_FAMILY, 24), text_color="white")
        logo_label.pack(pady=(45, 50), padx=30, anchor="w")

        # Sidebar Navigation Buttons
        nav_container = CTkFrame(master=sidebar, fg_color="transparent")
        nav_container.pack(fill=X, padx=15)

        btn_nav_home = CTkButton(master=nav_container, text="Dashboard", font=(FONT_FAMILY, 15), height=42, corner_radius=8,
                                 fg_color="transparent", text_color="white", hover_color=SIDEBAR_HOVER, anchor="w", command=show_home)
        btn_nav_home.pack(fill=X, pady=4)
        
        btn_nav_settings = CTkButton(master=nav_container, text="Shortcuts", font=(FONT_FAMILY, 15), height=42, corner_radius=8,
                                     fg_color="transparent", text_color="white", hover_color=SIDEBAR_HOVER, anchor="w", command=show_settings)
        btn_nav_settings.pack(fill=X, pady=4)

        # Bottom Footer in Sidebar
        footer_frame = CTkFrame(master=sidebar, fg_color="transparent")
        footer_frame.pack(side=BOTTOM, fill=X, pady=30, padx=15)

        btn_website = CTkButton(master=footer_frame, text="Visit Website", height=42, corner_radius=8, font=(FONT_FAMILY, 14),
                                fg_color="white", text_color=SIDEBAR_BG, hover_color="#F0F0F0", command=on_open_website)
        btn_website.pack(fill=X, pady=(0, 10))

        def close_and_exit():
            app.destroy()
            on_exit()

        btn_exit = CTkButton(master=footer_frame, text="Exit Application", height=42, corner_radius=8, font=(FONT_FAMILY, 14),
                             fg_color="transparent", text_color="#FFD6D6", border_width=1, border_color="#FFD6D6", hover_color="#FF4D4D", command=close_and_exit)
        btn_exit.pack(fill=X)

        # ==========================================
        # HOME TAB - Elegant White Cards
        # ==========================================
        CTkLabel(master=home_frame, text="Overview", font=(FONT_FAMILY, 28), text_color=TEXT_DARK).pack(anchor="w", pady=(0, 25))

        is_premium = is_premium_fn()
        status_text = "Premium Active" if is_premium else "Unlicensed Mode"
        status_color = "#22C55E" if is_premium else "#EF4444" 
        
        # Status Card
        status_card = CTkFrame(master=home_frame, fg_color=CARD_BG, corner_radius=12, border_width=1, border_color=BORDER_LIGHT)
        status_card.pack(fill=X, pady=(0, 20), ipadx=25, ipady=25)
        
        CTkLabel(master=status_card, text="License Status", font=(FONT_FAMILY, 13), text_color=TEXT_MUTED).pack(anchor="w", padx=20, pady=(10, 5))
        CTkLabel(master=status_card, text=status_text, font=(FONT_FAMILY, 22), text_color=status_color).pack(anchor="w", padx=20, pady=(0, 10))

        # Auto-Start Card
        system_card = CTkFrame(master=home_frame, fg_color=CARD_BG, corner_radius=12, border_width=1, border_color=BORDER_LIGHT)
        system_card.pack(fill=X, ipadx=25, ipady=20)

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        
        switch_frame = CTkFrame(master=system_card, fg_color="transparent")
        switch_frame.pack(fill=X, padx=20, pady=10)
        
        switch_info = CTkFrame(master=switch_frame, fg_color="transparent")
        switch_info.pack(side=LEFT)
        CTkLabel(master=switch_info, text="System Startup", font=(FONT_FAMILY, 15), text_color=TEXT_DARK).pack(anchor="w")
        CTkLabel(master=switch_info, text="Launch automatically in the background when Windows starts", font=(FONT_FAMILY, 13), text_color=TEXT_MUTED).pack(anchor="w")

        switch = CTkSwitch(master=switch_frame, text="", command=toggle_autostart, variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#E2E8F0", progress_color=SIDEBAR_BG, button_color="#FFFFFF", button_hover_color="#F8FAFC", switch_width=45, switch_height=24)
        switch.pack(side=RIGHT)

        # ==========================================
        # SETTINGS TAB - Clean Grid
        # ==========================================
        CTkLabel(master=settings_frame, text="Shortcuts", font=(FONT_FAMILY, 28), text_color=TEXT_DARK).pack(anchor="w", pady=(0, 10))
        CTkLabel(master=settings_frame, text="Modify your personal workflow keys. Hold 'Alt' to trigger.", font=(FONT_FAMILY, 14), text_color=TEXT_MUTED).pack(anchor="w", pady=(0, 25))

        grid_card = CTkFrame(master=settings_frame, fg_color=CARD_BG, corner_radius=12, border_width=1, border_color=BORDER_LIGHT)
        grid_card.pack(fill=BOTH, expand=True, ipadx=25, ipady=25)

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        
        entries = {}
        row, col = 0, 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_card, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=(15, 50), pady=12, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}", font=(FONT_FAMILY, 14), width=80, anchor="w", text_color=TEXT_DARK).pack(side=LEFT)
            
            entry = CTkEntry(master=field_frame, width=45, height=32, font=(FONT_FAMILY, 14), justify="center", 
                             fg_color="#F1F5F9", text_color=TEXT_DARK, border_width=0, corner_radius=6)
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

        save_btn = CTkButton(master=grid_card, text="Save Preferences", width=150, height=40, corner_radius=8, font=(FONT_FAMILY, 14), 
                             fg_color=SIDEBAR_BG, text_color="white", hover_color=SIDEBAR_HOVER, command=save_hotkeys)
        save_btn.grid(row=row+1, column=1, sticky="e", pady=(20, 0), padx=(0, 50))

        show_home()
        app.mainloop()
