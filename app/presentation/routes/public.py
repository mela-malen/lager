"""
Public routes - accessible without authentication.

This blueprint handles all public-facing pages including the landing page
and subscription flow.
"""

from flask import Blueprint, render_template, request

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
    email = request.form.get("email", "")
    name = request.form.get("name", "")

    # Använd business-lagret för hela prenumerationsflödet
    service = SubscriptionService()
    
    # Den här metoden kommer nu både validera och spara i databasen
    success, error = service.subscribe(email, name)

    if not success:
        # Om något gick fel (t.ex. ogiltig mejl eller om mejlen redan finns),
        # skicka tillbaka användaren till formuläret med felmeddelandet.
        return render_template(
            "subscribe.html",
            error=error,
            email=email,
            name=name,
        )

    # Prenumerationen sparades framgångsrikt - visa tack-sidan
    # Vi använder normaliserade värden för visningen
    normalized_email = service.normalize_email(email)
    normalized_name = service.normalize_name(name)

    return render_template(
        "thank_you.html",
        email=normalized_email,
        name=normalized_name,
    )