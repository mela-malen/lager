"""
Public routes - accessible without authentication.

This blueprint handles all public-facing pages including the landing page.
"""

from flask import Blueprint, render_template, request

# Här lägger vi till importen av din nya service
from app.business.services.subscription_service import SubscriptionService

bp = Blueprint("public", __name__)


@bp.route("/")
def index():
    """Render the landing page."""
    return render_template("index.html")


@bp.route("/subscribe")
def subscribe():
    """Render the subscription form."""
    return render_template("subscribe.html")


@bp.route("/subscribe/confirm", methods=["POST"])
def subscribe_confirm():
    """Handle subscription form submission."""
    # Hämta rådata från formuläret
    email = request.form.get("email", "")
    name = request.form.get("name", "")

    # Skapa en instans av din business-service
    service = SubscriptionService()

    # 1. Validera e-posten
    is_valid, error = service.validate_email(email)
    if not is_valid:
        # Om det inte är giltigt, skicka tillbaka användaren till formuläret
        # Vi skickar med 'error', 'email' och 'name' så att fältet inte töms
        return render_template(
            "subscribe.html",
            error=error,
            email=email,
            name=name,
        )

    # 2. Bearbeta datan (normalisera e-post/namn och lägg till tidsstämpel)
    # Här används din process_subscription-metod
    data = service.process_subscription(email, name)

    # Verifiering: skriver ut den STÄDADE datan i terminalen
    print(f"New subscription: {data['email']} ({data['name']}) vid {data['subscribed_at']}")

    # 3. Visa tack-sidan med den normaliserade datan
    return render_template("thank_you.html", email=data["email"], name=data["name"])