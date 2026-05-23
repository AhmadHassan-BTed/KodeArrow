"""Use cases define application-level business logic."""

from .navigation_action_use_case import NavigationAction, NavigationActionUseCase
from .unlock_premium_use_case import UnlockPremiumUseCase

__all__ = [
    "NavigationAction",
    "NavigationActionUseCase",
    "UnlockPremiumUseCase",
]
