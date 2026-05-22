from __future__ import annotations

import time


class UsageCollector:
    """Keeps in-memory telemetry counters (application layer)."""

    def __init__(self, *, multiplier: int):
        self.multiplier = multiplier
        self.stats = {
            "charactersTyped": 0,
            "kodeArrowHotkeys": 0,
            "TotalUsageMinutes": 0.0,

        }
        self.last_batch_time = time.time()

    def record_character(self) -> None:
        self.stats["charactersTyped"] += 1

    def record_hotkey(self) -> None:
        self.stats["kodeArrowHotkeys"] += 1

    def should_upload(self) -> bool:
        return self.stats["charactersTyped"] >= self.multiplier

    def reset_batch(self) -> None:
        now = time.time()
        interval_minutes = (now - self.last_batch_time) / 60
        self.stats["TotalUsageMinutes"] = float(self.stats["TotalUsageMinutes"]) + float(interval_minutes)


        self.stats["charactersTyped"] = 0
        self.stats["kodeArrowHotkeys"] = 0
        self.last_batch_time = now

