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
        
        # Make it a flyout window (no windows borders)
        app.overrideredirect(True)
        app.attributes("-topmost", True)
        
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        set_appearance_mode("Light")

        # Compact size like Lenovo Vantage
        w, h = 380, 680
        # Position at bottom right (above taskbar)
        x = ws - w - 15
        y = hs - h - 50 
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Colors based on existing theme + light mode Lenovo vibe
        HEADER_BG = "#4C7CFF" # Vibrant Blue header
        BG_COLOR = "#FAFAFA"
        TEXT_MAIN = "#1A1A1A"
        TEXT_SUB = "#666666"
        BORDER_COLOR = "#E0E0E0"
        FONT_FAMILY = "Bahnschrift" # Original font

        # Outer border frame to give the borderless window an edge
        main_border = CTkFrame(master=app, fg_color=BG_COLOR, border_width=1, border_color="#B0B0B0", corner_radius=0)
        main_border.pack(fill=BOTH, expand=True)

        # ------------------------------------------------
        # HEADER
        # ------------------------------------------------
        header = CTkFrame(master=main_border, fg_color=HEADER_BG, corner_radius=0, height=45)
        header.pack(fill=X)
        header.pack_propagate(False)

        title = CTkLabel(master=header, text="KodeArrow Settings", font=(FONT_FAMILY, 15), text_color="white")
        title.pack(side=LEFT, padx=15)

        btn_close = CTkButton(master=header, text="✕", width=35, height=35, fg_color="transparent", 
                              hover_color="#3A63CC", text_color="white", font=("Arial", 16), command=app.destroy)
        btn_close.pack(side=RIGHT, padx=5)

        # ------------------------------------------------
        # LICENSE STATUS SECTION
        # ------------------------------------------------
        # Title row with sub-link
        lic_header_frame = CTkFrame(master=main_border, fg_color="transparent")
        lic_header_frame.pack(fill=X, padx=20, pady=(20, 5))
        
        CTkLabel(master=lic_header_frame, text="LICENSE STATUS", font=(FONT_FAMILY, 11, "bold"), text_color=TEXT_MAIN).pack(side=LEFT)
        
        is_premium = is_premium_fn()
        
        # The big status block
        status_bg = "#E6FBE9" if is_premium else "#FBE6E6"
        status_border = "#34C759" if is_premium else "#FF3B30"
        status_text_color = "#28A745" if is_premium else "#DC3545"
        status_msg = "PREMIUM ACTIVE" if is_premium else "UNLICENSED"

        status_box = CTkFrame(master=main_border, fg_color=status_bg, border_color=status_border, border_width=2, corner_radius=6, height=75)
        status_box.pack(fill=X, padx=20)
        status_box.pack_propagate(False)
        
        # Emulating the big 100% text from the battery inspiration
        CTkLabel(master=status_box, text=status_msg, font=(FONT_FAMILY, 24, "bold"), text_color=status_text_color).pack(expand=True)

        # ------------------------------------------------
        # QUICK SHORTCUTS SECTION
        # ------------------------------------------------
        short_header_frame = CTkFrame(master=main_border, fg_color="transparent")
        short_header_frame.pack(fill=X, padx=20, pady=(25, 5))
        CTkLabel(master=short_header_frame, text="QUICK SHORTCUTS", font=(FONT_FAMILY, 11, "bold"), text_color=TEXT_MAIN).pack(side=LEFT)

        # Card container for shortcuts
        short_card = CTkFrame(master=main_border, fg_color="white", border_color=BORDER_COLOR, border_width=1, corner_radius=8)
        short_card.pack(fill=X, padx=20, ipadx=10, ipady=15)

        CTkLabel(master=short_card, text="Modifier: Alt + [Key]", font=(FONT_FAMILY, 12), text_color=TEXT_SUB).pack(pady=(0, 10))

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        entries = {}

        # Build a compact grid for the hotkeys inside the card
        grid_frame = CTkFrame(master=short_card, fg_color="transparent")
        grid_frame.pack(fill=BOTH, expand=True, padx=10)

        row, col = 0, 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_frame, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=10, pady=6, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}", font=(FONT_FAMILY, 13), width=65, anchor="w", text_color=TEXT_MAIN).pack(side=LEFT)
            
            entry = CTkEntry(master=field_frame, width=35, height=28, font=(FONT_FAMILY, 13), justify="center", 
                             fg_color="#F0F0F0", text_color=TEXT_MAIN, border_width=1, border_color="#D0D0D0", corner_radius=4)
            entry.insert(0, current_key)
            entry.pack(side=LEFT)
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
            save_btn.configure(text="SAVED")
            app.after(2000, lambda: save_btn.configure(text="APPLY SHORTCUTS"))

        save_btn = CTkButton(master=short_card, text="APPLY SHORTCUTS", width=120, height=30, corner_radius=4, font=(FONT_FAMILY, 12, "bold"), 
                             fg_color="transparent", text_color=HEADER_BG, border_width=1, border_color=HEADER_BG, hover_color="#E6EEFF", command=save_hotkeys)
        save_btn.pack(pady=(15, 0))

        # ------------------------------------------------
        # SYSTEM SETTINGS
        # ------------------------------------------------
        sys_header_frame = CTkFrame(master=main_border, fg_color="transparent")
        sys_header_frame.pack(fill=X, padx=20, pady=(25, 5))
        CTkLabel(master=sys_header_frame, text="SYSTEM", font=(FONT_FAMILY, 11, "bold"), text_color=TEXT_MAIN).pack(side=LEFT)

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        
        switch = CTkSwitch(master=main_border, text=" Auto-Start with Windows", command=toggle_autostart, variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#D0D0D0", progress_color=HEADER_BG, text_color=TEXT_MAIN, font=(FONT_FAMILY, 13))
        switch.pack(anchor="w", padx=20, pady=5)

        # ------------------------------------------------
        # BOTTOM FOOTER
        # ------------------------------------------------
        # Big pill button at the bottom
        btn_website = CTkButton(master=main_border, text="VISIT KODEARROW WEBSITE", height=45, corner_radius=22, font=(FONT_FAMILY, 13, "bold"),
                                fg_color=HEADER_BG, text_color="white", hover_color="#3A63CC", command=on_open_website)
        btn_website.pack(fill=X, padx=20, side=BOTTOM, pady=(0, 20))
        
        btn_exit = CTkButton(master=main_border, text="Quit KodeArrow Process", height=20, fg_color="transparent", text_color="#888888", 
                             hover_color=BG_COLOR, font=(FONT_FAMILY, 11, "underline"), command=lambda: [app.destroy(), on_exit()])
        btn_exit.pack(side=BOTTOM, pady=(0, 10))

        app.mainloop()
