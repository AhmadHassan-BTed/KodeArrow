from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Callable

from kode_arrow.application.use_cases.navigation_action_use_case import (
    NavigationAction,
    NavigationActionUseCase,
)
from kode_arrow.application.use_cases.telemetry.research_batching_service import (
    ResearchBatchingService,
)
from kode_arrow.application.use_cases.telemetry.upload_usage_use_case import (
    UploadUsageUseCase,
)
from kode_arrow.application.use_cases.telemetry.usage_collector import UsageCollector
from kode_arrow.application.use_cases.unlock_premium_use_case import UnlockPremiumUseCase
from kode_arrow.infrastructure.gui.dialog_adapter import DialogAdapter
from kode_arrow.infrastructure.gui.tray_adapter import TrayAdapter, TrayResources
from kode_arrow.infrastructure.keyboard.keyboard_adapter import KeyboardAdapter
from kode_arrow.infrastructure.keyboard.keypress_adapter import KeypressAdapter
from kode_arrow.infrastructure.services.firebase_telemetry_adapter import FirebaseTelemetryAdapter
from kode_arrow.infrastructure.services.subscription_premium_adapter import (
    SubscriptionPremiumAdapter,
)


@dataclass(frozen=True)
class REditionDeps:
    keyboard: KeyboardAdapter
    keypress: KeypressAdapter
    dialog: DialogAdapter
    premium: SubscriptionPremiumAdapter
    telemetry: FirebaseTelemetryAdapter
    collector: UsageCollector
    batching: ResearchBatchingService


def _icon_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "assets",
        "branding",
        "icon.ico",
    )


def build_reedition_app_deps(*, premium_file_provider: Callable[[], str]) -> REditionDeps:
    keyboard = KeyboardAdapter()
    keypress = KeypressAdapter()
    dialog = DialogAdapter()

    premium = SubscriptionPremiumAdapter(premium_file_provider=premium_file_provider)
    telemetry = FirebaseTelemetryAdapter()

    multiplier = 20
    collector = UsageCollector(multiplier=multiplier)

    uploader = UploadUsageUseCase(
        telemetry_port=telemetry,
        collection="ControlGroup",
        email="research_user@example.com",
    )

    batching = ResearchBatchingService(collector=collector, uploader=uploader)

    return REditionDeps(
        keyboard=keyboard,
        keypress=keypress,
        dialog=dialog,
        premium=premium,
        telemetry=telemetry,
        collector=collector,
        batching=batching,
    )


def build_reedition_navigation_use_case(*, is_premium: bool, keypress_port: KeypressAdapter) -> NavigationActionUseCase:
    return NavigationActionUseCase(is_premium=is_premium, keypress_port=keypress_port)


def build_reedition_tray(
    *,
    icon_path: str,
    deps: REditionDeps,
    hardware_id: str,
    premium_file_path: str,
    is_premium: bool,
    open_portfolio: Callable[[], None],
    open_website: Callable[[], None],
    open_portal: Callable[[], None],
    show_research_info: Callable[[], None],
    stop_app: Callable[[], None],
) -> TrayAdapter:
    tray = TrayAdapter(
        resources=TrayResources(icon_path=icon_path),
        on_open_creator_links=open_portfolio,
    )

    def on_exit() -> None:
        stop_app()

    def on_unlock() -> None:
        def on_email_submit(email: str) -> None:
            use_case = UnlockPremiumUseCase(
                premium_port=deps.premium,
                hardware_id=hardware_id,
                premium_file_path=premium_file_path,
                is_research=True,
            )
            result = use_case.execute(email=email)
            if result.success:
                deps.dialog.show_message(
                    "Success",
                    "Premium access unlocked! Please restart the application to apply changes.",
                )
            else:
                deps.dialog.show_error("Unlock Failed", f"Error: {result.message}")

        deps.dialog.show_email_input_dialog(on_email_submit)

    tray.build_menu(
        is_premium=is_premium,
        on_unlock=on_unlock if not is_premium else None,
        on_exit=on_exit,
        on_open_portfolio=open_portfolio,
        on_open_website=open_website,
        on_show_research_info=show_research_info,
        on_open_portal=open_portal,
    )

    return tray


def reedition_icon_path() -> str:
    return _icon_path()


def now_seconds() -> float:
    return time.time()

