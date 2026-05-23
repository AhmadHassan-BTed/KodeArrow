import os
from PIL import Image, ImageDraw
from customtkinter import (CTk, CTkFrame, CTkLabel, CTkButton, CTkSwitch, CTkEntry, CTkImage,
                         BOTH, LEFT, RIGHT, TOP, BOTTOM, X, Y, StringVar, set_appearance_mode)
from kode_arrow.utils.resource import get_resource_path
from kode_arrow.utils.system import enable_autostart, disable_autostart, is_autostart_enabled
from kode_arrow.config.user_prefs import UserPrefs

def create_gradient_bg(width, height, radius):
    img = Image.new("RGBA", (2, 2))
    img.putpixel((0, 0), (0, 71, 255, 255))   # Bright blue top left
    img.putpixel((1, 0), (0, 45, 200, 255)) 
    img.putpixel((0, 1), (0, 25, 120, 255)) 
    img.putpixel((1, 1), (5, 15, 65, 255))    # Deep navy bottom right
    img = img.resize((width, height), Image.Resampling.BICUBIC)
    
    # Rounded corners using alpha mask
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
    
    alpha = Image.new('L', img.size, 255)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    img.putalpha(alpha)
    return img

class DashboardWindow:
    @staticmethod
    def open(is_premium_fn, on_open_website, on_exit, on_reload_engine, on_unlock):
        app = CTk()
        app.title("KodeArrow Dashboard")
        app.iconbitmap(get_resource_path(os.path.join('assets', 'branding', 'icon.ico')))
        
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        set_appearance_mode("Light")
        app.resizable(False, False)

        w, h = 950, 600
        app.geometry('%dx%d+%d+%d' % (w, h, (ws/2)-(w/2), (hs/2)-(h/2)))

        FONT_FAMILY = "Segoe UI"
        BG_MAIN = "#F0F2F6" # Slightly darker light-gray to make white cards pop
        
        container = CTkFrame(master=app, fg_color=BG_MAIN, corner_radius=0)
        container.pack(fill=BOTH, expand=True)

        # ------------------------------------------------
        # SIDEBAR (Gradient & Floating)
        # ------------------------------------------------
        sidebar_width = 280
        sidebar_height = 570 # h - 30
        
        sidebar_margin = CTkFrame(master=container, fg_color="transparent", width=sidebar_width, height=sidebar_height)
        sidebar_margin.pack(side=LEFT, fill=Y, pady=15, padx=(15, 0))
        sidebar_margin.pack_propagate(False)

        # Gradient Background Image
        grad_img = create_gradient_bg(sidebar_width, sidebar_height, 20)
        grad_ctk = CTkImage(light_image=grad_img, size=(sidebar_width, sidebar_height))
        # Important: Store image reference in the widget to prevent garbage collection
        sidebar_bg = CTkLabel(master=sidebar_margin, text="", image=grad_ctk, width=sidebar_width, height=sidebar_height)
        sidebar_bg.image = grad_ctk 
        sidebar_bg.place(x=0, y=0)

        # Sidebar Content Overlay
        sidebar = CTkFrame(master=sidebar_margin, fg_color="transparent", bg_color="transparent")
        sidebar.place(x=0, y=0, relwidth=1, relheight=1)

        # Logo Section
        logo_frame = CTkFrame(master=sidebar, fg_color="transparent")
        logo_frame.pack(fill=X, pady=(40, 40), padx=25)
        
        icon_box = CTkFrame(master=logo_frame, width=45, height=45, corner_radius=12, fg_color="#0047FF", border_width=1, border_color="#3370FF")
        icon_box.pack(side=LEFT)
        icon_box.pack_propagate(False)
        CTkLabel(master=icon_box, text="+", font=(FONT_FAMILY, 28), text_color="white").pack(expand=True)
        
        text_frame = CTkFrame(master=logo_frame, fg_color="transparent")
        text_frame.pack(side=LEFT, padx=15)
        CTkLabel(master=text_frame, text="KodeArrow® 2023", font=(FONT_FAMILY, 15, "bold"), text_color="white").pack(anchor="w")
        CTkLabel(master=text_frame, text="a project by Ahmad Hassan", font=(FONT_FAMILY, 10), text_color="#A0B5E8").pack(anchor="w")

        # Navigation
        nav_container = CTkFrame(master=sidebar, fg_color="transparent")
        nav_container.pack(fill=X, padx=20)

        btn_nav_home = CTkButton(master=nav_container, text="   ⌂   Dashboard", font=(FONT_FAMILY, 13, "bold"), height=42, corner_radius=10,
                                 fg_color="#0035D0", text_color="white", hover_color="#0047FF", anchor="w")
        btn_nav_home.pack(fill=X, pady=5)
        
        btn_nav_settings = CTkButton(master=nav_container, text="   ⌘   Shortcuts", font=(FONT_FAMILY, 13), height=42, corner_radius=10,
                                     fg_color="transparent", text_color="#D0DFFF", hover_color="#0035D0", anchor="w")
        btn_nav_settings.pack(fill=X, pady=5)

        # Bottom Buttons
        footer_frame = CTkFrame(master=sidebar, fg_color="transparent")
        footer_frame.pack(side=BOTTOM, fill=X, pady=30, padx=20)

        btn_website = CTkButton(master=footer_frame, text="Visit Website         →", height=42, corner_radius=10, font=(FONT_FAMILY, 12, "bold"),
                                fg_color="#0047FF", text_color="white", hover_color="#0035D0", command=on_open_website)
        btn_website.pack(fill=X, pady=(0, 15))

        btn_exit = CTkButton(master=footer_frame, text="Exit Application      →", height=42, corner_radius=10, font=(FONT_FAMILY, 12),
                             fg_color="transparent", text_color="white", border_width=1, border_color="#4D7AFF", hover_color="#002599", command=lambda: [app.destroy(), on_exit()])
        btn_exit.pack(fill=X)

        # ------------------------------------------------
        # MAIN CONTENT AREA
        # ------------------------------------------------
        main_content = CTkFrame(master=container, fg_color="transparent")
        main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=50, pady=40)

        home_frame = CTkFrame(master=main_content, fg_color="transparent")
        settings_frame = CTkFrame(master=main_content, fg_color="transparent")

        def show_home():
            settings_frame.pack_forget()
            home_frame.pack(fill=BOTH, expand=True)
            btn_nav_home.configure(fg_color="#0035D0", text_color="white", font=(FONT_FAMILY, 13, "bold"))
            btn_nav_settings.configure(fg_color="transparent", text_color="#D0DFFF", font=(FONT_FAMILY, 13))

        def show_settings():
            home_frame.pack_forget()
            settings_frame.pack(fill=BOTH, expand=True)
            btn_nav_settings.configure(fg_color="#0035D0", text_color="white", font=(FONT_FAMILY, 13, "bold"))
            btn_nav_home.configure(fg_color="transparent", text_color="#D0DFFF", font=(FONT_FAMILY, 13))

        btn_nav_home.configure(command=show_home)
        btn_nav_settings.configure(command=show_settings)

        # ==========================================
        # HOME TAB
        # ==========================================
        CTkLabel(master=home_frame, text="Overview", font=(FONT_FAMILY, 28, "bold"), text_color="#001B4D").pack(anchor="w", pady=(0, 5))
        CTkFrame(master=home_frame, width=35, height=4, fg_color="#0047FF", corner_radius=2).pack(anchor="w", pady=(0, 30))

        is_premium = is_premium_fn()
        
        # License Card
        lic_card = CTkFrame(master=home_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        lic_card.pack(fill=X, pady=(0, 20), ipadx=25, ipady=25)
        
        lic_header = CTkFrame(master=lic_card, fg_color="transparent")
        lic_header.pack(fill=X)
        badge = CTkFrame(master=lic_header, fg_color="#FDE8E8" if not is_premium else "#E1FDE8", corner_radius=6, width=28, height=28)
        badge.pack(side=LEFT)
        badge.pack_propagate(False)
        CTkLabel(master=badge, text="!" if not is_premium else "✓", text_color="#F05252" if not is_premium else "#22C55E", font=(FONT_FAMILY, 14, "bold")).pack(expand=True)
        CTkLabel(master=lic_header, text="License Status", font=(FONT_FAMILY, 13), text_color="#4B5563").pack(side=LEFT, padx=12)

        lic_body = CTkFrame(master=lic_card, fg_color="transparent")
        lic_body.pack(fill=X, pady=(15, 0))
        
        status_color = "#E02424" if not is_premium else "#059669"
        CTkLabel(master=lic_body, text="Unlicensed Mode" if not is_premium else "Premium Active", font=(FONT_FAMILY, 20, "bold"), text_color=status_color).pack(side=LEFT)
        
        if not is_premium:
            btn_unlock = CTkButton(master=lic_body, text="♛  Unlock Premium", height=40, corner_radius=8, font=(FONT_FAMILY, 12, "bold"),
                                   fg_color="#0047FF", text_color="white", hover_color="#0035D0", command=on_unlock)
            btn_unlock.pack(side=RIGHT)
            
            pill = CTkFrame(master=lic_card, fg_color="#FDE8E8", corner_radius=10, height=22)
            pill.pack(anchor="w", pady=(12, 0))
            pill.pack_propagate(False)
            CTkLabel(master=pill, text="•  Limited Features Available", font=(FONT_FAMILY, 10), text_color="#E02424").pack(padx=10, expand=True)

        # Startup Card
        sys_card = CTkFrame(master=home_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        sys_card.pack(fill=X, ipadx=25, ipady=20)

        sys_header = CTkFrame(master=sys_card, fg_color="transparent")
        sys_header.pack(fill=X)
        badge2 = CTkFrame(master=sys_header, fg_color="#E1EFFE", corner_radius=6, width=32, height=32)
        badge2.pack(side=LEFT)
        badge2.pack_propagate(False)
        CTkLabel(master=badge2, text="🚀", font=("Segoe UI Emoji", 16)).pack(expand=True)
        
        text_col = CTkFrame(master=sys_header, fg_color="transparent")
        text_col.pack(side=LEFT, padx=12)
        CTkLabel(master=text_col, text="System Startup", font=(FONT_FAMILY, 14, "bold"), text_color="#111827").pack(anchor="w")
        CTkLabel(master=text_col, text="Launch KodeArrow automatically in the background when Windows starts", font=(FONT_FAMILY, 11), text_color="#6B7280").pack(anchor="w")

        switch_frame = CTkFrame(master=sys_card, fg_color="transparent")
        switch_frame.pack(fill=X, pady=(20, 0))

        def toggle_autostart():
            if switch_var.get() == "on": enable_autostart()
            else: disable_autostart()
            update_switch_text()

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")
        switch = CTkSwitch(master=switch_frame, text="", command=toggle_autostart, variable=switch_var, onvalue="on", offvalue="off",
                           fg_color="#D1D5DB", progress_color="#0047FF", text_color="#111827", font=(FONT_FAMILY, 13), switch_width=40, switch_height=20)
        switch.pack(side=LEFT)

        def update_switch_text():
            switch.configure(text="   Enabled" if switch_var.get() == "on" else "   Disabled")
        update_switch_text()

        # ==========================================
        # SETTINGS TAB
        # ==========================================
        CTkLabel(master=settings_frame, text="Shortcuts", font=(FONT_FAMILY, 28, "bold"), text_color="#001B4D").pack(anchor="w", pady=(0, 5))
        CTkFrame(master=settings_frame, width=35, height=4, fg_color="#0047FF", corner_radius=2).pack(anchor="w", pady=(0, 15))
        CTkLabel(master=settings_frame, text="Modify your personal workflow keys. Hold 'Alt' to trigger.", font=(FONT_FAMILY, 12), text_color="#6B7280").pack(anchor="w", pady=(0, 25))

        grid_card = CTkFrame(master=settings_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        grid_card.pack(fill=BOTH, expand=True, ipadx=25, ipady=25)

        prefs = UserPrefs.load()
        hotkeys = prefs.get("hotkeys", {})
        
        entries = {}
        row, col = 0, 0
        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_card, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=(0, 50), pady=12, sticky="w")
            
            CTkLabel(master=field_frame, text=f"{action.capitalize()}:", font=(FONT_FAMILY, 13), width=65, anchor="w", text_color="#374151").pack(side=LEFT)
            
            entry = CTkEntry(master=field_frame, width=40, height=30, font=(FONT_FAMILY, 13), justify="center", 
                             fg_color="#F9FAFB", text_color="#111827", border_width=1, border_color="#D1D5DB", corner_radius=6)
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
            save_btn.configure(text="✓  Changes Saved")
            app.after(2500, lambda: save_btn.configure(text="Save Preferences"))

        save_btn = CTkButton(master=grid_card, text="Save Preferences", width=140, height=38, corner_radius=8, font=(FONT_FAMILY, 12, "bold"), 
                             fg_color="#0047FF", text_color="white", hover_color="#0035D0", command=save_hotkeys)
        save_btn.grid(row=row+1, column=1, sticky="e", pady=(25, 0))

        show_home()
        app.mainloop()
