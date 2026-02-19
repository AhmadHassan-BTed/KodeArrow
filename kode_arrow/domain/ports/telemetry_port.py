from __future__ import annotations

from typing import Protocol


class TelemetryPort(Protocol):
    def upload_usage_data(self, *, collection: str, email: str, data: dict) -> bool:
        ...

