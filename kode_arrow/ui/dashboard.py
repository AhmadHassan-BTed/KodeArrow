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
        app.title("KodeArrow")
        app.iconbitmap(get_resource_path(os.path.join('assets', 'branding', 'icon.ico')))
        
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        set_appearance_mode("Light")
        app.resizable(False, False)

        w, h = 900, 600
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))

        # SaaS-inspired Minimalist Color Palette
        BG_APP = "#f4f5f7"          # Soft warm-gray app background (Arc/macOS style)
        BG_SURFACE = "#ffffff"      # Pure white floating cards
        PRIMARY_BLUE = "#0A5CFF"    # Rich, modern tech blue
        HOVER_BLUE = "#0047E0"      
        TEXT_TITLE = "#1A1B20"      # Off-black headings
        TEXT_MUTED = "#6B6D76"      # Soft elegant gray for subtext
        TEXT_INPUT = "#3F4045"
        BORDER_SOFT = "#E9EAEE"     # Barely visible card borders

        FONT_FAMILY = "Segoe UI"
        
        container = CTkFrame(master=app, fg_color=BG_APP)
        container.pack(fill=BOTH, expand=True)

        # ------------------------------------------------
        # SIDEBAR (Floating panel appearance)
        # ------------------------------------------------
        # To simulate a floating sidebar, we give it a margin (padx, pady) 
        # and rounded corners over the main background
        sidebar_margin = CTkFrame(master=container, width=220, fg_color="transparent")
        sidebar_margin.pack(side=LEFT, fill=Y, pady=25, padx=(25, 10))

        sidebar = CTkFrame(master=sidebar_margin, width=220, fg_color=BG_SURFACE, corner_radius=16, border_width=1, border_color=BORDER_SOFT)
        sidebar.pack(fill=BOTH, expand=True)
        sidebar.pack_propagate(False) # Keep width fixed

        # ------------------------------------------------
        # MAIN CONTENT (Airy and spacious)
        # ------------------------------------------------
        main_content = CTkFrame(master=container, fg_color="transparent")
        main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=40, pady=25)

        home_frame = CTkFrame(master=main_content, fg_color="transparent")
        settings_frame = CTkFrame(master=main_content, fg_color="transparent")

        # Sidebar State Management
        btn_nav_home = None
        btn_nav_settings = None

        def update_nav_styles(active_tab):
            # Pill-shaped active state
            default_fg = "transparent"
            active_fg = "#F0F2F5"
            default_text = TEXT_MUTED
            active_text = PRIMARY_BLUE

            btn_nav_home.configure(fg_color=active_fg if active_tab == "home" else default_fg, 
                                   text_color=active_text if active_tab == "home" else default_text)
            btn_nav_settings.configure(fg_color=active_fg if active_tab == "settings" else default_fg,
                                       text_color=active_text if active_tab == "settings" else default_text)

        def show_home():
            settings_frame.pack_forget()
            home_frame.pack(fill=BOTH, expand=True)
            update_nav_styles("home")

        def show_settings():
            home_frame.pack_forget()
            settings_frame.pack(fill=BOTH, expand=True)
            update_nav_styles("settings")

        # Sidebar Branding
        logo_label = CTkLabel(master=sidebar, text="KodeArrow", font=(FONT_FAMILY, 18, "bold"), text_color=TEXT_TITLE)
        logo_label.pack(pady=(40, 40), padx=25, anchor="w")

        # Nav Buttons (Pill-shaped, soft hover)
        nav_container = CTkFrame(master=sidebar, fg_color="transparent")
        nav_container.pack(fill=X, padx=15)

        btn_nav_home = CTkButton(master=nav_container, text="Overview", font=(FONT_FAMILY, 14), height=38, corner_radius=19,
                                 fg_color="transparent", text_color=TEXT_MUTED, hover_color="#F8F9FB", anchor="w", command=show_home)
        btn_nav_home.pack(fill=X, pady=4)
        
        btn_nav_settings = CTkButton(master=nav_container, text="Shortcuts", font=(FONT_FAMILY, 14), height=38, corner_radius=19,
                                     fg_color="transparent", text_color=TEXT_MUTED, hover_color="#F8F9FB", anchor="w", command=show_settings)
        btn_nav_settings.pack(fill=X, pady=4)

        # ==========================================
        # HOME TAB - Elegant Cards
        # ==========================================
        CTkLabel(master=home_frame, text="Overview", font=(FONT_FAMILY, 28), text_color=TEXT_TITLE).pack(anchor="w", pady=(20, 30))

        is_premium = is_premium_fn()
        status_text = "Premium Active" if is_premium else "Unlicensed Mode"
        status_color = "#34C759" if is_premium else "#FF6B6B" # Softer modern red
        
        # License Card (Soft shadow simulation via light border, rounded corners)
        status_card = CTkFrame(master=home_frame, fg_color=BG_SURFACE, corner_radius=16, border_width=1, border_color=BORDER_SOFT)
        status_card.pack(fill=X, pady=(0, 25), ipadx=25, ipady=25)
        
        CTkLabel(master=status_card, text="License Status", font=(FONT_FAMILY, 13), text_color=TEXT_MUTED).pack(anchor="w", padx=25, pady=(15, 2))
        CTkLabel(master=status_card, text=status_text, font=(FONT_FAMILY, 20), text_color=status_color).pack(anchor="w", padx=25, pady=(0, 15))

        # Auto-Start Card
        system_card = CTkFrame(master=home_frame, fg_color=BG_SURFACE, corner_radius=16, border_width=1, border_color=BORDER_SOFT)
        system_card.pack(fill=X, ipadx=25, ipady=15)

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        
        switch_frame = CTkFrame(master=system_card, fg_color="transparent")
        switch_frame.pack(fill=X, padx=25, pady=15)
        
        switch_info = CTkFrame(master=switch_frame, fg_color="transparent")
        switch_info.pack(side=LEFT)
        CTkLabel(master=switch_info, text="System Startup", font=(FONT_FAMILY, 15), text_color=TEXT_TITLE).pack(anchor="w")
        CTkLabel(master=switch_info, text="Launch KodeArrow smoothly in the background when Windows starts", font=(FONT_FAMILY, 12), text_color=TEXT_MUTED).pack(anchor="w")

        # Modern iOS-style switch
        switch = CTkSwitch(master=switch_frame, text="", command=toggle_autostart, variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#E9E9EA", progress_color="#34C759", button_color="#FFFFFF", button_hover_color="#F4F5F7", switch_width=44, switch_height=24)
        switch.pack(side=RIGHT, pady=5)

        # ==========================================
        # SETTINGS TAB - Clean Grid
        # ==========================================
        CTkLabel(master=settings_frame, text="Shortcuts", font=(FONT_FAMILY, 28), text_color=TEXT_TITLE).pack(anchor="w", pady=(20, 8))
        CTkLabel(master=settings_frame, text="Modify your personal workflow keys. Hold 'Alt' to trigger.", font=(FONT_FAMILY, 14), text_color=TEXT_MUTED).pack(anchor="w", pady=(0, 40))

        grid_card = CTkFrame(master=settings_frame, fg_color=BG_SURFACE, corner_radius=16, border_width=1, border_color=BORDER_SOFT)
        grid_card.pack(fill=BOTH, expand=True, ipadx=20, ipady=20)

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        
        entries = {}
        row, col = 0, 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_card, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=(20, 60), pady=12, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}", font=(FONT_FAMILY, 14), width=80, anchor="w", text_color=TEXT_TITLE).pack(side=LEFT)
            
            # Refined Entry Box
            entry = CTkEntry(master=field_frame, width=45, height=34, font=(FONT_FAMILY, 14), justify="center", 
                             fg_color="#F4F5F7", text_color=TEXT_INPUT, border_width=0, corner_radius=8)
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

        save_btn = CTkButton(master=grid_card, text="Save Preferences", width=150, height=38, corner_radius=19, font=(FONT_FAMILY, 13), 
                             fg_color=PRIMARY_BLUE, text_color="white", hover_color=HOVER_BLUE, command=save_hotkeys)
        save_btn.grid(row=row+1, column=1, sticky="e", pady=(20, 0), padx=(0, 60))

        # ==========================================
        # BOTTOM FOOTER (Sidebar)
        # ==========================================
        footer_frame = CTkFrame(master=sidebar, fg_color="transparent")
        footer_frame.pack(side=BOTTOM, fill=X, pady=25, padx=20)

        # Elegant solid filled buttons
        btn_website = CTkButton(master=footer_frame, text="Visit Website", height=38, corner_radius=10, font=(FONT_FAMILY, 13),
                                fg_color=PRIMARY_BLUE, text_color="white", hover_color=HOVER_BLUE, command=on_open_website)
        btn_website.pack(fill=X, pady=(0, 10))

        def close_and_exit():
            app.destroy()
            on_exit()

        btn_exit = CTkButton(master=footer_frame, text="Exit App", height=38, corner_radius=10, font=(FONT_FAMILY, 13),
                             fg_color="#F4F5F7", text_color="#E03A3A", hover_color="#E8E9EB", command=close_and_exit)
        btn_exit.pack(fill=X)

        show_home()
        app.mainloop()
