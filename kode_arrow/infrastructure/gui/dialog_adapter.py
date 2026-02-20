from __future__ import annotations

from typing import Callable

from kode_arrow.domain.ports.dialog_port import DialogPort
from kode_arrow.presentation.dialogs import DialogManager
from tkinter import messagebox


class DialogAdapter(DialogPort):
    def show_email_input_dialog(self, on_submit_callback: Callable[[str], None]) -> None:
        DialogManager.show_email_input_dialog(on_submit_callback)

    def show_message(self, title: str, message: str) -> None:
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message)