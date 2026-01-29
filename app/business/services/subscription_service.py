import re
from datetime import datetime, timezone

class SubscriptionService:
    """Service for handling subscription-related business logic."""

    # Email regex pattern for validation
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format."""
        if not email or not email.strip():
            return False, "Email is required"
        if not re.match(self.EMAIL_PATTERN, email.strip()):
            return False, "Invalid email format"
        return True, ""

    def normalize_email(self, email: str) -> str:
        """Normalize email address (lowercase and strip whitespace)."""
        return email.lower().strip()

    def normalize_name(self, name: str | None) -> str:
        """Normalize name field, defaults to 'Subscriber'."""
        if not name or not name.strip():
            return "Subscriber"
        return name.strip()

    def process_subscription(self, email: str, name: str | None) -> dict:
        """Validates, normalizes, and packages data for storage."""
        # Validate first
        is_valid, error = self.validate_email(email)
        if not is_valid:
            raise ValueError(error)

        # Normalize and package
        return {
            "email": self.normalize_email(email),
            "name": self.normalize_name(name),
            "subscribed_at": datetime.now(timezone.utc).isoformat(),
        }