"""
Configuration settings for the ShopEase test framework.
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Credentials:
    """Holds email and password for a user role."""
    email: str
    password: str


@dataclass
class Viewport:
    """Browser viewport dimensions."""
    width: int
    height: int


class Settings:
    """Centralized configuration for the test framework using Singleton pattern."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):

        config_path = Path(__file__).parent.parent / "config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.base_url = os.environ.get("TEST_BASE_URL", data["base_url"])
        self.timeout = int(os.environ.get("TEST_TIMEOUT", data["timeout"]))
        self.viewport = Viewport(**data["viewport"])

        self.customer = Credentials(**data["credentials"]["customer"])
        self.vip = Credentials(**data["credentials"]["vip"])

    @property
    def default_email(self) -> str:
        """Default user email for most tests."""
        return self.customer.email

    @property
    def default_password(self) -> str:
        """Default password for most tests."""
        return self.customer.password