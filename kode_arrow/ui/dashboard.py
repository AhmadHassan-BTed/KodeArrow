import os
import zipfile
from io import BytesIO
from typing import Callable, cast
import importlib.resources as resources

import lucide
from PIL import Image, ImageDraw, ImageFont
from customtkinter import (
    CTk, CTkFrame, CTkLabel, CTkButton, CTkSwitch, CTkEntry,
    CTkImage, BOTH, LEFT, RIGHT, TOP, BOTTOM, X, Y, StringVar,
    set_appearance_mode
)
from kode_arrow.utils.resource import get_resource_path
from kode_arrow.utils.system import enable_autostart, disable_autostart, is_autostart_enabled
from kode_arrow.config.user_prefs import UserPrefs

# ─────────────────────────────────────────────────────────────────────────────
# Icon loader — renders Lucide SVGs from the installed lucide package.
# SVGs are read from lucide.zip and rasterized with CairoSVG.
# ─────────────────────────────────────────────────────────────────────────────



def _load_emoji_icon(emoji_char, size=16):
    img = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
    try:
        font = ImageFont.truetype('C:\\Windows\\Fonts\\seguiemj.ttf', size + 2)
        draw = ImageDraw.Draw(img)
        draw.text((size // 2, size // 2), emoji_char, font=font, embedded_color=True)
    except Exception:
        pass
    return CTkImage(light_image=img, dark_image=img, size=(size, size))

class DashboardWindow:
    @staticmethod
    def open(is_premium_fn, on_open_website, on_exit, on_reload_engine, on_unlock):
        app = CTk()
        app.title("KodeArrow")
        app.iconbitmap(get_resource_path(os.path.join("assets", "branding", "icon.ico")))

        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        app.resizable(False, False)

        w, h = 940, 580
        app.geometry("%dx%d+%d+%d" % (w, h, (ws / 2) - (w / 2), (hs / 2) - (h / 2)))

        def on_closing():
            app.withdraw()
            app.quit()
        app.protocol("WM_DELETE_WINDOW", on_closing)

        # ── Theme palettes ────────────────────────────────────────────────────
        THEMES = {
            "light": {
                "BG_APP":           "#F5F7FA",
                "BG_SURFACE":       "#FFFFFF",
                "BG_SIDEBAR":       "#FFFFFF",
                "BORDER":           "#E5E7EB",
                "TEXT_PRIMARY":     "#111827",
                "TEXT_SECONDARY":   "#6B7280",
                "TEXT_MUTED":       "#9CA3AF",
                "TEXT_INPUT":       "#374151",
                "ACCENT":           "#00207f",
                "ACCENT_HOVER":     "#00134c",
                "DANGER":           "#EF4444",
                "SWITCH_OFF":       "#CBD5E1",
                "SWITCH_ON":        "#00207f",
                "SWITCH_BTN":       "#FFFFFF",
                "SWITCH_BTN_HOVER": "#EFF6FF",
                "NAV_ACTIVE_BG":    "#EFF6FF",
                "NAV_ACTIVE_TEXT":  "#00207f",
                "NAV_HOVER":        "#F1F5F9",
                "BTN_EXIT_BG":      "#F9FAFB",
                "BTN_EXIT_TEXT":    "#DC2626",
                "BTN_EXIT_HOVER":   "#FEF2F2",
                "TAG_BG_RED":       "#FFF1F2",
                "TAG_TEXT_RED":     "#E11D48",
                "TAG_BG_BLUE":      "#EFF6FF",
                "TAG_TEXT_BLUE":    "#00207f",
                "ENTRY_BG":         "#F8FAFC",
                "SEP":              "#E5E7EB",
                # theme-toggle button colours (shows "switch to dark")
                "THEME_BG":         "#F0F2F5",
                "THEME_HOVER":      "#E5E7EB",
                "THEME_TEXT":       "#374151",
                # icon stroke colours
                "ICON_NAV":         "#9CA3AF",
                "ICON_NAV_ACTIVE":  "#00207f",
                "ICON_CARD":        "#00207f",
                "ICON_WEB":         "#FFFFFF",
                "ICON_EXIT":        "#DC2626",
                "ICON_THEME":       "#374151",
            },
            "dark": {
                "BG_APP":           "#18181B",
                "BG_SURFACE":       "#27272A",
                "BG_SIDEBAR":       "#1F1F22",
                "BORDER":           "#3F3F46",
                "TEXT_PRIMARY":     "#E4E4E7",
                "TEXT_SECONDARY":   "#A1A1AA",
                "TEXT_MUTED":       "#71717A",
                "TEXT_INPUT":       "#D4D4D8",
                "ACCENT":           "#3B82F6",
                "ACCENT_HOVER":     "#2563EB",
                "DANGER":           "#F87171",
                "SWITCH_OFF":       "#3F3F46",
                "SWITCH_ON":        "#3B82F6",
                "SWITCH_BTN":       "#FAFAFA",
                "SWITCH_BTN_HOVER": "#E4E4E7",
                "NAV_ACTIVE_BG":    "#27272A",
                "NAV_ACTIVE_TEXT":  "#60A5FA",
                "NAV_HOVER":        "#27272A",
                "BTN_EXIT_BG":      "#27272A",
                "BTN_EXIT_TEXT":    "#FCA5A5",
                "BTN_EXIT_HOVER":   "#3F3F46",
                "TAG_BG_RED":       "#451A1E",
                "TAG_TEXT_RED":     "#FCA5A5",
                "TAG_BG_BLUE":      "#1E3A8A",
                "TAG_TEXT_BLUE":    "#93C5FD",
                "ENTRY_BG":         "#18181B",
                "SEP":              "#3F3F46",
                "THEME_BG":         "#27272A",
                "THEME_HOVER":      "#3F3F46",
                "THEME_TEXT":       "#E4E4E7",
                "ICON_NAV":         "#A1A1AA",
                "ICON_NAV_ACTIVE":  "#60A5FA",
                "ICON_CARD":        "#60A5FA",
                "ICON_WEB":         "#E4E4E7",
                "ICON_EXIT":        "#FCA5A5",
                "ICON_THEME":       "#E4E4E7",
            },
        }

        FONT         = "Segoe UI"
        prefs        = UserPrefs.load()
        mode         = {"v": prefs.get("theme", "light")}   # single mutable dict — avoids closure issues
        _rebuild_ref: list[Callable[[], None] | None] = [None]

        def T(key):
            return THEMES[mode["v"]][key]

        ICO = {
            "nav_overview_inactive": _load_emoji_icon("🏠", 16),
            "nav_overview_active":   _load_emoji_icon("🏠", 16),
            "nav_shortcuts_inactive":_load_emoji_icon("⌨️", 16),
            "nav_shortcuts_active":  _load_emoji_icon("⌨️", 16),
            "sun":                   _load_emoji_icon("☀️", 16),
            "moon":                  _load_emoji_icon("🌙", 16),
            "globe":                 _load_emoji_icon("🌐", 15),
            "power":                 _load_emoji_icon("🚪", 15),
            "shield":                _load_emoji_icon("🛡️", 20),
            "rocket":                _load_emoji_icon("🚀", 20),
        }
        def ico(key):
            """Return the CTkImage for the current theme mode."""
            return ICO[key]

        # ── Root ──────────────────────────────────────────────────────────────
        set_appearance_mode("Dark" if mode["v"] == "dark" else "Light")

        root_frame = CTkFrame(master=app, fg_color=T("BG_APP"), corner_radius=0)
        root_frame.pack(fill=BOTH, expand=True)

        # ══════════════════════════════════════════════════════════════════════
        # SIDEBAR
        # ══════════════════════════════════════════════════════════════════════
        sidebar_wrap = CTkFrame(master=root_frame, fg_color="transparent", width=210)
        sidebar_wrap.pack(side=LEFT, fill=Y)
        sidebar_wrap.pack_propagate(False)

        sidebar = CTkFrame(
            master=sidebar_wrap, fg_color=T("BG_SIDEBAR"),
            corner_radius=0, border_width=1, border_color=T("BORDER")
        )
        sidebar.pack(fill=BOTH, expand=True)

        # ── Logo row: "KodeArrow" left · theme-toggle button right ────────────
        LOGO_PADX = 18   # used for logo row AND divider — keeps them aligned

        logo_row = CTkFrame(master=sidebar, fg_color="transparent")
        logo_row.pack(fill=X, padx=LOGO_PADX, pady=(26, 0))

        # Left group: dot + name
        logo_left = CTkFrame(master=logo_row, fg_color="transparent")
        logo_left.pack(side=LEFT)

        logo_dot = CTkFrame(master=logo_left, width=7, height=7,
                            fg_color=T("ACCENT"), corner_radius=4)
        logo_dot.pack(side=LEFT, pady=3)
        logo_dot.pack_propagate(False)

        logo_label = CTkLabel(
            master=logo_left, text="KodeArrow",
            font=(FONT, 14, "bold"), text_color=T("TEXT_PRIMARY")
        )
        logo_label.pack(side=LEFT, padx=(7, 0))

        # Right: compact square icon button (sun / moon)
        def _theme_icon():
            # in light → show moon (clicking goes dark); in dark → show sun
            return ico("moon") if mode["v"] == "light" else ico("sun")

        def toggle_theme():
            mode["v"] = "dark" if mode["v"] == "light" else "light"
            p = UserPrefs.load()
            p["theme"] = mode["v"]
            UserPrefs.save(p)
            if _rebuild_ref[0]:
                _rebuild_ref[0]()

        theme_btn = CTkButton(
            master=logo_row,
            text="", image=ico("moon") if mode["v"] == "light" else ico("sun"),
            width=28, height=28,
            corner_radius=6,
            fg_color=T("THEME_BG"),
            hover_color=T("THEME_HOVER"),
            command=toggle_theme,
        )
        theme_btn.pack(side=RIGHT)

        # ── Divider ───────────────────────────────────────────────────────────
        div1 = CTkFrame(master=sidebar, height=1, fg_color=T("BORDER"), corner_radius=0)
        div1.pack(fill=X, padx=LOGO_PADX, pady=(20, 14))

        nav_section_lbl = CTkLabel(
            master=sidebar, text="NAVIGATION",
            font=(FONT, 9), text_color=T("TEXT_MUTED")
        )
        nav_section_lbl.pack(anchor="w", padx=22, pady=(0, 5))

        # ── Nav ───────────────────────────────────────────────────────────────
        nav_container = CTkFrame(master=sidebar, fg_color="transparent")
        nav_container.pack(fill=X, padx=10, pady=(0, 4))

        current_tab = {"v": "home"}

        main_wrapper = CTkFrame(master=root_frame, fg_color=T("BG_APP"), corner_radius=0)
        main_wrapper.pack(side=LEFT, fill=BOTH, expand=True)

        home_frame     = CTkFrame(master=main_wrapper, fg_color="transparent")
        settings_frame = CTkFrame(master=main_wrapper, fg_color="transparent")

        btn_nav_home = btn_nav_settings = None   # assigned after creation

        def update_nav(active):
            for btn, key, ico_base in [
                (btn_nav_home,     "home",     "nav_overview"),
                (btn_nav_settings, "settings", "nav_shortcuts"),
            ]:
                if btn is None:
                    continue
                is_active = (key == active)
                btn.configure(
                    image=ico(f"{ico_base}_active" if is_active else f"{ico_base}_inactive"),
                    fg_color=T("NAV_ACTIVE_BG") if is_active else "transparent",
                    text_color=T("NAV_ACTIVE_TEXT") if is_active else T("TEXT_SECONDARY"),
                    hover_color=T("NAV_ACTIVE_BG") if is_active else T("NAV_HOVER"),
                )

        def show_home():
            current_tab["v"] = "home"
            settings_frame.pack_forget()
            home_frame.pack(fill=BOTH, expand=True, padx=36, pady=28)
            update_nav("home")

        def show_settings():
            current_tab["v"] = "settings"
            home_frame.pack_forget()
            settings_frame.pack(fill=BOTH, expand=True, padx=36, pady=28)
            update_nav("settings")

        NAV_ITEMS = [
            ("home",     "  Overview",  show_home,     "nav_overview"),
            ("settings", "  Shortcuts", show_settings, "nav_shortcuts"),
        ]

        nav_buttons = {}
        for key, label, cmd, ico_base in NAV_ITEMS:
            btn = CTkButton(
                master=nav_container, text=label, image=ico(f"{ico_base}_inactive"), compound="left",
                font=(FONT, 13), height=34, corner_radius=7,
                fg_color="transparent",
                text_color=T("TEXT_SECONDARY"),
                hover_color=T("NAV_HOVER"),
                anchor="w",
                command=cmd,
            )
            btn.pack(fill=X, pady=2)
            nav_buttons[key] = btn

        btn_nav_home     = nav_buttons["home"]
        btn_nav_settings = nav_buttons["settings"]

        # ── Sidebar footer ────────────────────────────────────────────────────
        footer = CTkFrame(master=sidebar, fg_color="transparent")
        footer.pack(side=BOTTOM, fill=X, pady=18, padx=10)

        btn_website = CTkButton(
            master=footer, text="  Visit Website", image=ico("globe"), compound="left",
            height=34, corner_radius=7, font=(FONT, 12),
            fg_color=T("ACCENT"), text_color="#FFFFFF",
            hover_color=T("ACCENT_HOVER"), command=on_open_website,
        )
        btn_website.pack(fill=X, pady=(0, 5))

        def close_and_exit():
            app.withdraw()
            app.quit()
            on_exit()

        btn_exit = CTkButton(
            master=footer, text="  Exit KodeArrow", image=ico("power"), compound="left",
            height=34, corner_radius=7, font=(FONT, 12),
            fg_color=T("BTN_EXIT_BG"),
            text_color=T("BTN_EXIT_TEXT"),
            hover_color=T("BTN_EXIT_HOVER"),
            command=close_and_exit,
        )
        btn_exit.pack(fill=X)

        # ══════════════════════════════════════════════════════════════════════
        # HOME TAB
        # ══════════════════════════════════════════════════════════════════════
        header_frame = CTkFrame(master=home_frame, fg_color="transparent")
        header_frame.pack(fill=X, pady=(0, 22))

        home_title = CTkLabel(
            master=header_frame, text="Overview",
            font=(FONT, 21, "bold"), text_color=T("TEXT_PRIMARY")
        )
        home_title.pack(anchor="w")

        home_sub = CTkLabel(
            master=header_frame,
            text="Manage your license and system preferences",
            font=(FONT, 12), text_color=T("TEXT_MUTED"),
        )
        home_sub.pack(anchor="w", pady=(2, 0))

        # ── License card ──────────────────────────────────────────────────────
        is_premium = is_premium_fn()

        status_card = CTkFrame(
            master=home_frame, fg_color=T("BG_SURFACE"),
            corner_radius=12, border_width=1, border_color=T("BORDER")
        )
        status_card.pack(fill=X, pady=(0, 14))

        status_inner = CTkFrame(master=status_card, fg_color="transparent")
        status_inner.pack(fill=X, padx=22, pady=18)

        shield_lbl = CTkLabel(master=status_inner, text="", image=ico("shield"))
        shield_lbl.pack(side=LEFT, padx=(0, 14))

        left_status = CTkFrame(master=status_inner, fg_color="transparent")
        left_status.pack(side=LEFT, fill=X, expand=True)

        status_label_title = CTkLabel(
            master=left_status, text="License Status",
            font=(FONT, 10), text_color=T("TEXT_SECONDARY"),
        )
        status_label_title.pack(anchor="w")

        status_value_label = CTkLabel(
            master=left_status,
            text="Premium Active" if is_premium else "Unlicensed",
            font=(FONT, 17, "bold"),
            text_color=T("ACCENT") if is_premium else T("DANGER"),
        )
        status_value_label.pack(anchor="w", pady=(3, 0))

        badge = CTkLabel(
            master=left_status,
            text="● Active" if is_premium else "● Inactive",
            font=(FONT, 10),
            text_color=T("TAG_TEXT_BLUE") if is_premium else T("TAG_TEXT_RED"),
            fg_color=T("TAG_BG_BLUE")   if is_premium else T("TAG_BG_RED"),
            corner_radius=4, padx=7, pady=2,
        )
        badge.pack(anchor="w", pady=(5, 0))

        btn_unlock = CTkButton(
            master=status_inner, text="Unlock Premium →",
            height=32, corner_radius=7, font=(FONT, 12),
            fg_color=T("ACCENT"), text_color="#FFFFFF",
            hover_color=T("ACCENT_HOVER"), command=None,
        )
        if not is_premium:
            btn_unlock.pack(side=RIGHT, padx=(14, 0))

        def refresh_license_status():
            is_prem = is_premium_fn()
            status_value_label.configure(
                text="Premium Active" if is_prem else "Unlicensed",
                text_color=T("ACCENT") if is_prem else T("DANGER")
            )
            badge.configure(
                text="● Active" if is_prem else "● Inactive",
                text_color=T("TAG_TEXT_BLUE") if is_prem else T("TAG_TEXT_RED"),
                fg_color=T("TAG_BG_BLUE") if is_prem else T("TAG_BG_RED")
            )
            if is_prem:
                try:
                    btn_unlock.pack_forget()
                except Exception:
                    pass
            else:
                try:
                    btn_unlock.pack(side=RIGHT, padx=(14, 0))
                except Exception:
                    pass

        def handle_unlock():
            on_unlock(on_success=lambda: app.after(0, refresh_license_status))

        btn_unlock.configure(command=handle_unlock)

        # ── Startup card ──────────────────────────────────────────────────────
        startup_card = CTkFrame(
            master=home_frame, fg_color=T("BG_SURFACE"),
            corner_radius=12, border_width=1, border_color=T("BORDER")
        )
        startup_card.pack(fill=X)

        startup_inner = CTkFrame(master=startup_card, fg_color="transparent")
        startup_inner.pack(fill=X, padx=22, pady=18)

        rocket_lbl = CTkLabel(master=startup_inner, text="", image=ico("rocket"))
        rocket_lbl.pack(side=LEFT, padx=(0, 14))

        startup_left = CTkFrame(master=startup_inner, fg_color="transparent")
        startup_left.pack(side=LEFT, expand=True, fill=X)

        startup_title = CTkLabel(
            master=startup_left, text="Launch on System Startup",
            font=(FONT, 13, "bold"), text_color=T("TEXT_PRIMARY"),
        )
        startup_title.pack(anchor="w")

        startup_sub = CTkLabel(
            master=startup_left,
            text="Starts silently in the background when Windows boots",
            font=(FONT, 11), text_color=T("TEXT_SECONDARY"),
        )
        startup_sub.pack(anchor="w", pady=(3, 0))

        switch_var = StringVar(value="on" if is_autostart_enabled() else "off")

        def toggle_autostart():
            (enable_autostart if switch_var.get() == "on" else disable_autostart)()

        autostart_switch = CTkSwitch(
            master=startup_inner, text="",
            command=toggle_autostart,
            variable=switch_var, onvalue="on", offvalue="off",
            fg_color=T("SWITCH_OFF"), progress_color=T("SWITCH_ON"),
            button_color=T("SWITCH_BTN"), button_hover_color=T("SWITCH_BTN_HOVER"),
            switch_width=40, switch_height=22,
        )
        autostart_switch.pack(side=RIGHT)

        # ══════════════════════════════════════════════════════════════════════
        # SETTINGS TAB
        # ══════════════════════════════════════════════════════════════════════
        header_s = CTkFrame(master=settings_frame, fg_color="transparent")
        header_s.pack(fill=X, pady=(0, 22))

        settings_title = CTkLabel(
            master=header_s, text="Shortcuts",
            font=(FONT, 21, "bold"), text_color=T("TEXT_PRIMARY"),
        )
        settings_title.pack(anchor="w")

        settings_sub = CTkLabel(
            master=header_s,
            text="Hold  Alt  +  your key  to trigger an action",
            font=(FONT, 12), text_color=T("TEXT_SECONDARY"),
        )
        settings_sub.pack(anchor="w", pady=(2, 0))

        grid_card = CTkFrame(
            master=settings_frame, fg_color=T("BG_SURFACE"),
            corner_radius=12, border_width=1, border_color=T("BORDER")
        )
        grid_card.pack(fill=BOTH, expand=True)

        grid_inner = CTkFrame(master=grid_card, fg_color="transparent")
        grid_inner.pack(fill=BOTH, expand=True, padx=28, pady=24)
        grid_inner.columnconfigure(0, weight=1)
        grid_inner.columnconfigure(1, weight=1)

        # Base key selector/input
        base_key_frame = CTkFrame(master=grid_inner, fg_color="transparent")
        base_key_frame.grid(row=0, column=0, columnspan=2, padx=(0, 24), pady=(0, 16), sticky="w")
        
        base_key_lbl = CTkLabel(
            master=base_key_frame, text="Modifier / Base Key:  ",
            font=(FONT, 12, "bold"), text_color=T("TEXT_PRIMARY")
        )
        base_key_lbl.pack(side=LEFT)
        
        base_key_val = prefs.get("modifier", "alt")
        base_key_combo = CTkComboBox(
            master=base_key_frame, values=["alt", "ctrl", "shift", "windows"],
            width=100, height=28, font=(FONT, 11, "bold"),
            fg_color=T("ENTRY_BG"), text_color=T("TEXT_INPUT"),
            border_color=T("BORDER"), button_color=T("ACCENT"),
            button_hover_color=T("ACCENT_HOVER"), corner_radius=6
        )
        base_key_combo.set(base_key_val)
        base_key_combo.pack(side=LEFT)

        prefs        = UserPrefs.load()
        hotkeys      = prefs.get("hotkeys", {})
        entries      = {}
        entry_widgets = []
        row_i, col   = 1, 0

        for action, current_key in hotkeys.items():
            field_frame = CTkFrame(master=grid_inner, fg_color="transparent")
            field_frame.grid(row=row_i, column=col, padx=(0, 24), pady=10, sticky="ew")
            field_frame.columnconfigure(0, weight=1)

            lbl = CTkLabel(
                master=field_frame,
                text=action.replace("_", " ").capitalize(),
                font=(FONT, 12), text_color=T("TEXT_SECONDARY"), anchor="w",
            )
            lbl.grid(row=0, column=0, sticky="w")

            alt_lbl = CTkLabel(
                master=field_frame, text=f"{base_key_val.capitalize()} +",
                font=(FONT, 11), text_color=T("TEXT_MUTED"),
            )
            alt_lbl.grid(row=0, column=1, padx=(8, 4))

            ent = CTkEntry(
                master=field_frame, width=42, height=30,
                font=(FONT, 13, "bold"), justify="center",
                fg_color=T("ENTRY_BG"), text_color=T("TEXT_INPUT"),
                border_width=1, border_color=T("BORDER"), corner_radius=6,
            )
            ent.insert(0, current_key)
            ent.grid(row=0, column=2)

            entries[action] = ent
            entry_widgets.append((lbl, alt_lbl, ent))

            col += 1
            if col > 1:
                col, row_i = 0, row_i + 1

        sep = CTkFrame(master=grid_inner, height=1, fg_color=T("SEP"))
        sep.grid(row=row_i + 1, column=0, columnspan=2, sticky="ew", pady=(20, 14))

        def save_hotkeys():
            new_prefs = prefs.copy()
            new_prefs["modifier"] = base_key_combo.get().strip().lower()
            for action, entry in entries.items():
                val = entry.get().strip().lower()
                if len(val) == 1:
                    new_prefs["hotkeys"][action] = val
            UserPrefs.save(new_prefs)
            on_reload_engine()
            
            # Update prefix labels
            new_mod = base_key_combo.get().strip().capitalize()
            for _, alt_w, _ in entry_widgets:
                alt_w.configure(text=f"{new_mod} +")
                
            save_btn.configure(text="✓  Saved")
            app.after(2200, lambda: save_btn.configure(text="Save Preferences"))

        def reset_hotkeys():
            from kode_arrow.config.user_prefs import DEFAULT_PREFS
            base_key_combo.set(DEFAULT_PREFS["modifier"])
            for action, default_key in DEFAULT_PREFS["hotkeys"].items():
                if action in entries:
                    entries[action].delete(0, END)
                    entries[action].insert(0, default_key)
            new_prefs = prefs.copy()
            new_prefs["hotkeys"] = DEFAULT_PREFS["hotkeys"].copy()
            new_prefs["modifier"] = DEFAULT_PREFS["modifier"]
            UserPrefs.save(new_prefs)
            on_reload_engine()
            
            # Reset prefix labels to default modifier
            default_mod = DEFAULT_PREFS["modifier"].capitalize()
            for _, alt_w, _ in entry_widgets:
                alt_w.configure(text=f"{default_mod} +")
                
            reset_btn.configure(text="✓  Reset Done")
            app.after(2200, lambda: reset_btn.configure(text="Reset to Defaults"))

        reset_btn = CTkButton(
            master=grid_inner, text="Reset to Defaults",
            width=145, height=34, corner_radius=7,
            font=(FONT, 12), fg_color="#F3F4F6" if mode["v"] == "light" else "#374151",
            text_color="#1F2937" if mode["v"] == "light" else "#F3F4F6",
            hover_color="#E5E7EB" if mode["v"] == "light" else "#4B5563",
            command=reset_hotkeys,
        )
        reset_btn.grid(row=row_i + 2, column=0, sticky="w", pady=(0, 2))

        save_btn = CTkButton(
            master=grid_inner, text="Save Preferences",
            width=155, height=34, corner_radius=7,
            font=(FONT, 12), fg_color=T("ACCENT"),
            text_color="#FFFFFF", hover_color=T("ACCENT_HOVER"),
            command=save_hotkeys,
        )
        save_btn.grid(row=row_i + 2, column=1, sticky="e", pady=(0, 2))

        # ══════════════════════════════════════════════════════════════════════
        # _rebuild_ui — called after every theme toggle
        # All icon variants are pre-rendered; we just swap .configure() calls.
        # No cairosvg work happens here → zero lag.
        # ══════════════════════════════════════════════════════════════════════
        def _rebuild_ui():
            m = mode["v"]
            set_appearance_mode("Dark" if m == "dark" else "Light")

            # Structure
            root_frame.configure(fg_color=T("BG_APP"))
            main_wrapper.configure(fg_color=T("BG_APP"))
            sidebar.configure(fg_color=T("BG_SIDEBAR"), border_color=T("BORDER"))
            div1.configure(fg_color=T("BORDER"))
            logo_dot.configure(fg_color=T("ACCENT"))
            logo_label.configure(text_color=T("TEXT_PRIMARY"))
            nav_section_lbl.configure(text_color=T("TEXT_MUTED"))

            # Theme button
            theme_btn.configure(
                text="", 
                image=ico("moon") if mode["v"] == "light" else ico("sun"),
                fg_color=T("THEME_BG"),
                hover_color=T("THEME_HOVER"),
            )

            update_nav(current_tab["v"])

            # Footer
            btn_website.configure(fg_color=T("ACCENT"), hover_color=T("ACCENT_HOVER"))
            btn_exit.configure(

                fg_color=T("BTN_EXIT_BG"),
                text_color=T("BTN_EXIT_TEXT"),
                hover_color=T("BTN_EXIT_HOVER"),
            )

            # Card icons
            # shield_lbl.configure()
            # rocket_lbl.configure()

            # Home
            status_card.configure(fg_color=T("BG_SURFACE"), border_color=T("BORDER"))
            startup_card.configure(fg_color=T("BG_SURFACE"), border_color=T("BORDER"))
            home_title.configure(text_color=T("TEXT_PRIMARY"))
            home_sub.configure(text_color=T("TEXT_MUTED"))
            status_label_title.configure(text_color=T("TEXT_SECONDARY"))
            status_value_label.configure(
                text_color=T("ACCENT") if is_premium_fn() else T("DANGER")
            )
            badge.configure(
                fg_color  =T("TAG_BG_BLUE")    if is_premium_fn() else T("TAG_BG_RED"),
                text_color=T("TAG_TEXT_BLUE")  if is_premium_fn() else T("TAG_TEXT_RED"),
            )
            startup_title.configure(text_color=T("TEXT_PRIMARY"))
            startup_sub.configure(text_color=T("TEXT_SECONDARY"))
            autostart_switch.configure(
                fg_color=T("SWITCH_OFF"), progress_color=T("SWITCH_ON"),
                button_color=T("SWITCH_BTN"), button_hover_color=T("SWITCH_BTN_HOVER"),
            )

            # Settings
            settings_title.configure(text_color=T("TEXT_PRIMARY"))
            settings_sub.configure(text_color=T("TEXT_SECONDARY"))
            grid_card.configure(fg_color=T("BG_SURFACE"), border_color=T("BORDER"))
            sep.configure(fg_color=T("SEP"))
            save_btn.configure(fg_color=T("ACCENT"), hover_color=T("ACCENT_HOVER"))
            reset_btn.configure(
                fg_color="#F3F4F6" if m == "light" else "#374151",
                text_color="#1F2937" if m == "light" else "#F3F4F6",
                hover_color="#E5E7EB" if m == "light" else "#4B5563"
            )
            base_key_lbl.configure(text_color=T("TEXT_PRIMARY"))
            base_key_combo.configure(
                fg_color=T("ENTRY_BG"),
                text_color=T("TEXT_INPUT"),
                border_color=T("BORDER"),
                button_color=T("ACCENT"),
                button_hover_color=T("ACCENT_HOVER")
            )

            for lbl_w, alt_w, ent_w in entry_widgets:
                lbl_w.configure(text_color=T("TEXT_SECONDARY"))
                alt_w.configure(text_color=T("TEXT_MUTED"))
                ent_w.configure(
                    fg_color=T("ENTRY_BG"),
                    text_color=T("TEXT_INPUT"),
                    border_color=T("BORDER"),
                )

        _rebuild_ref[0] = _rebuild_ui

        # ── Boot ──────────────────────────────────────────────────────────────
        show_home()
        app.mainloop()