from __future__ import annotations

from kode_arrow.domain.ports.telemetry_port import TelemetryPort
from kode_arrow.common.services.firebase_service import FirebaseService


class FirebaseTelemetryAdapter(TelemetryPort):
    def __init__(self):
        self._service = FirebaseService()

    def upload_usage_data(self, *, collection: str, email: str, data: dict) -> bool:
        return self._service.upload_usage_data(collection, email, data)

