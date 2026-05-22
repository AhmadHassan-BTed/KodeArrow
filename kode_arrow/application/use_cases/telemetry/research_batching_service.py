from __future__ import annotations


class ResearchBatchingService:
    """Orchestrates collector + uploader when thresholds are reached."""

    def __init__(self, *, collector, uploader, on_uploaded=None):
        self._collector = collector
        self._uploader = uploader
        self._on_uploaded = on_uploaded

    @property
    def stats(self) -> dict:
        return self._collector.stats

    def record_character_and_maybe_upload(self) -> None:
        self._collector.record_character()
        if self._collector.should_upload():
            self._upload_and_reset()

    def record_hotkey(self) -> None:
        self._collector.record_hotkey()

    def _upload_and_reset(self) -> None:
        data_snapshot = dict(self._collector.stats)
        self._uploader.execute(data=data_snapshot)
        self._collector.reset_batch()
        if self._on_uploaded:
            self._on_uploaded()

