"""Service infrastructure - external API clients and their port adapters."""

from .firebase import FirebaseService
from .subscription import SubscriptionService
from .firebase_telemetry_adapter import FirebaseTelemetryAdapter
from .subscription_premium_adapter import SubscriptionPremiumAdapter

__all__ = [
    "FirebaseService",
    "SubscriptionService",
    "FirebaseTelemetryAdapter",
    "SubscriptionPremiumAdapter",
]
