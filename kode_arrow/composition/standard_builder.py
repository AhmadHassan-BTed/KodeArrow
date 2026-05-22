from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

from kode_arrow.application.use_cases.navigation_action_use_case import (
    NavigationAction,
    NavigationActionUseCase,
)
from kode_arrow.application.use_cases.unlock_premium_use_case import (
    UnlockPremiumUseCase,
)
from kode_arrow.infrastructure.gui.dialog_adapter import DialogAdapter
from kode_arrow.infrastructure.gui.tray_adapter import TrayAdapter, TrayResources
from kode_arrow.infrastructure.keyboard.keyboard_adapter import KeyboardAdapter
from kode_arrow.infrastructure.keyboard.keypress_adapter import KeypressAdapter
from kode_arrow.infrastructure.services.firebase_telemetry_adapter import FirebaseTelemetryAdapter
from kode_arrow.infrastructure.services.subscription_premium_adapter import (
    SubscriptionPremiumAdapter,
)


@dataclass(frozen=True)
class StandardEditionDeps:
    keyboard: KeyboardAdapter
    keypress: KeypressAdapter
    dialog: DialogAdapter
    premium: SubscriptionPremiumAdapter
    telemetry: FirebaseTelemetryAdapter


def _icon_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "assets",
        "branding",
        "icon.ico",
    )


def build_standard_app_deps(*, premium_file_provider: Callable[[], str]) -> StandardEditionDeps:
    keyboard = KeyboardAdapter()
    keypress = KeypressAdapter()
    dialog = DialogAdapter()

    premium = SubscriptionPremiumAdapter(premium_file_provider=premium_file_provider)
    telemetry = FirebaseTelemetryAdapter()

    return StandardEditionDeps(
        keyboard=keyboard,
        keypress=keypress,
        dialog=dialog,
        premium=premium,
        telemetry=telemetry,
    )


