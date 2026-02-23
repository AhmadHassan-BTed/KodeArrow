import time

class TelemetryService:
    """Collects and batches usage stats, uploading to Firebase when thresholds are reached."""

    def __init__(self, firebase_service, email: str, multiplier: int, on_uploaded=None):
        self.firebase = firebase_service
        self.email = email
        self.multiplier = multiplier
        self.on_uploaded = on_uploaded
        self.stats = {
            "charactersTyped": 0,
            "kodeArrowHotkeys": 0,
            "TotalUsageMinutes": 0.0,
        }
        self.last_batch_time = time.time()

    def record_character(self) -> None:
        self.stats["charactersTyped"] += 1
        if self.stats["charactersTyped"] >= self.multiplier:
            self.upload_and_reset()

    def record_hotkey(self) -> None:
        self.stats["kodeArrowHotkeys"] += 1

    def upload_and_reset(self) -> None:
        now = time.time()
        interval_minutes = (now - self.last_batch_time) / 60
        self.stats["TotalUsageMinutes"] = float(self.stats["TotalUsageMinutes"]) + float(interval_minutes)

        data_snapshot = dict(self.stats)
        self.firebase.upload_usage_data(
            collection="ControlGroup",
            email=self.email,
            data=data_snapshot
        )

        self.stats["charactersTyped"] = 0
        self.stats["kodeArrowHotkeys"] = 0
        self.last_batch_time = now

        if self.on_uploaded:
            self.on_uploaded()
