"""GUI infrastructure layer - adapts domain ports to UI frameworks."""

from .dialog_adapter import DialogAdapter
from .tray_adapter import TrayAdapter, TrayResources

__all__ = [
    "DialogAdapter",
    "TrayAdapter",
    "TrayResources",
]
