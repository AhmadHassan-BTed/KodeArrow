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

        w, h = 800, 550
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))

        # Define Colors (Minimalist Modern)
        BG_COLOR = "#f9f9fb" # Very light gray/blue, clean canvas
        SIDEBAR_COLOR = "#ffffff"
        PRIMARY_BLUE = "#0047FF" # A more modern, vibrant electric blue
        HOVER_BLUE = "#0035bf"
        TEXT_MAIN = "#1d1d1f" # Apple-style off-black
        TEXT_MUTED = "#86868b"

        # Modern Thin Font Stack
        FONT_FAMILY = "Segoe UI"
        
        # Container
        container = CTkFrame(master=app, fg_color=BG_COLOR)
        container.pack(fill=BOTH, expand=True)

        # Sidebar with subtle right border effect (using a wrapper frame)
        sidebar_wrapper = CTkFrame(master=container, width=220, fg_color="#e5e5e5", corner_radius=0)
        sidebar_wrapper.pack(side=LEFT, fill=Y)
        
        sidebar = CTkFrame(master=sidebar_wrapper, width=219, fg_color=SIDEBAR_COLOR, corner_radius=0)
        sidebar.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 1))

        # Main Content Area
        main_content = CTkFrame(master=container, fg_color=BG_COLOR, corner_radius=0)
        main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=50, pady=50)

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
        logo_label = CTkLabel(master=sidebar, text="KodeArrow", font=(FONT_FAMILY, 24), text_color=TEXT_MAIN)
        logo_label.pack(pady=(50, 60))

        # Sidebar Navigation Buttons (More padding, thin font)
        btn_nav_home = CTkButton(master=sidebar, text="Overview", font=(FONT_FAMILY, 15), height=40, fg_color="transparent", text_color=TEXT_MAIN, hover_color="#f0f0f5", anchor="w", command=show_home)
        btn_nav_home.pack(fill=X, padx=15, pady=5)
        
        btn_nav_settings = CTkButton(master=sidebar, text="Shortcuts", font=(FONT_FAMILY, 15), height=40, fg_color="transparent", text_color=TEXT_MAIN, hover_color="#f0f0f5", anchor="w", command=show_settings)
        btn_nav_settings.pack(fill=X, padx=15, pady=5)

        # ==========================================
        # HOME TAB
        # ==========================================
        title = CTkLabel(master=home_frame, text="Overview", font=(FONT_FAMILY, 32), text_color=TEXT_MAIN)
        title.pack(anchor="w", pady=(0, 40))

        is_premium = is_premium_fn()
        status_text = "Premium Active" if is_premium else "Unlicensed Mode"
        status_color = "#34c759" if is_premium else "#ff3b30"
        
        status_box = CTkFrame(master=home_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#ebebeb")
        status_box.pack(fill=X, pady=(0, 30), ipadx=20, ipady=25)
        
        CTkLabel(master=status_box, text="Current License Status", font=(FONT_FAMILY, 14), text_color=TEXT_MUTED).pack(anchor="w", padx=20, pady=(15, 5))
        CTkLabel(master=status_box, text=status_text, font=(FONT_FAMILY, 24), text_color=status_color).pack(anchor="w", padx=20, pady=(0, 15))

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        switch = CTkSwitch(master=home_frame, text=" Start seamlessly with Windows", command=toggle_autostart,
                           variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#e5e5e5", progress_color=PRIMARY_BLUE, text_color=TEXT_MAIN, font=(FONT_FAMILY, 15))
        switch.pack(anchor="w", pady=10)

        # ==========================================
        # SETTINGS TAB
        # ==========================================
        CTkLabel(master=settings_frame, text="Shortcuts", font=(FONT_FAMILY, 32), text_color=TEXT_MAIN).pack(anchor="w", pady=(0, 10))
        CTkLabel(master=settings_frame, text="Hold the 'Alt' modifier key to trigger these actions.", font=(FONT_FAMILY, 14), text_color=TEXT_MUTED).pack(anchor="w", pady=(0, 40))

        grid_frame = CTkFrame(master=settings_frame, fg_color="transparent")
        grid_frame.pack(fill=BOTH, expand=True)

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        
        entries = {}
        row = 0
        col = 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_frame, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=(0, 60), pady=15, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}:", font=(FONT_FAMILY, 15), width=90, anchor="w", text_color=TEXT_MAIN).pack(side=LEFT)
            entry = CTkEntry(master=field_frame, width=60, height=35, font=(FONT_FAMILY, 15), justify="center", fg_color="#f5f5f7", text_color=TEXT_MAIN, border_width=1, border_color="#d2d2d7", corner_radius=8)
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
            
            save_btn.configure(text="Saved successfully")
            app.after(2000, lambda: save_btn.configure(text="Save Changes"))

        save_btn = CTkButton(master=settings_frame, text="Save Changes", width=160, height=40, corner_radius=20, font=(FONT_FAMILY, 14), fg_color=PRIMARY_BLUE, text_color="white", hover_color=HOVER_BLUE, command=save_hotkeys)
        save_btn.pack(anchor="e", pady=30)

        # ==========================================
        # BOTTOM FOOTER (Global to sidebar)
        # ==========================================
        footer_frame = CTkFrame(master=sidebar, fg_color="transparent")
        footer_frame.pack(side=BOTTOM, fill=X, pady=40, padx=20)

        # Modern Filled Buttons (Primary and Secondary styling)
        btn_website = CTkButton(master=footer_frame, text="Visit Website", height=40, corner_radius=8, font=(FONT_FAMILY, 14),
                                fg_color=PRIMARY_BLUE, text_color="white", hover_color=HOVER_BLUE, command=on_open_website)
        btn_website.pack(fill=X, pady=(0, 15))

        def close_and_exit():
            app.destroy()
            on_exit()

        btn_exit = CTkButton(master=footer_frame, text="Exit Application", height=40, corner_radius=8, font=(FONT_FAMILY, 14),
                             fg_color="#f2f2f7", text_color="#ff3b30", hover_color="#e5e5ea", command=close_and_exit)
        btn_exit.pack(fill=X)

        # Start on Home
        show_home()
        app.mainloop()
