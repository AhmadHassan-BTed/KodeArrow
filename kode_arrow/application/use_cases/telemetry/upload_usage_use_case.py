from __future__ import annotations


class UploadUsageUseCase:
    def __init__(self, *, telemetry_port, collection: str, email: str):
        self._telemetry_port = telemetry_port
        self._collection = collection
        self._email = email

    def execute(self, *, data: dict) -> bool:
        return self._telemetry_port.upload_usage_data(
            collection=self._collection,
            email=self._email,
            data=data,
        )

