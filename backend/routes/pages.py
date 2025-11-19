from __future__ import annotations

from datetime import datetime

from flask import Blueprint, render_template, abort, redirect, url_for

from ..db import db
from ..models import Event, Registration, Role
from .utils import login_required, get_current_user

pages_bp = Blueprint("pages", __name__)


@pages_bp.app_errorhandler(403)
def forbidden(_):
    return render_template("errors/403.html"), 403


@pages_bp.route("/")
def landing():
    events = Event.query.order_by(Event.start_date).limit(3).all()
    return render_template("landing.html", featured_events=events)


@pages_bp.route("/portal/dashboard")
@login_required()
def dashboard():
    stats = {
        "total_events": Event.query.count(),
        "total_registrations": Registration.query.count(),
        "active_events": Event.query.filter(Event.status == "active").count(),
        "pending_registrations": Registration.query.filter(
            Registration.status == "pending"
        ).count(),
    }
    latest_registrations = (
        Registration.query.order_by(Registration.created_at.desc()).limit(5).all()
    )
    return render_template(
        "pages/dashboard.html",
        stats=stats,
        latest_registrations=latest_registrations,
        events=Event.query.limit(6).all(),
    )


@pages_bp.route("/portal")
@login_required()
def portal_home():
    return redirect(url_for("pages.dashboard"))


@pages_bp.route("/portal/registrations")
@login_required(roles=[Role.ADMIN, Role.MANAGER, Role.STAFF, Role.STUDENT])
def student_registrations():
    user = get_current_user()

    if user and user.role == Role.STUDENT:
        registrations = Registration.query.filter_by(email=user.email).all()
    else:
        registrations = Registration.query.order_by(
            Registration.created_at.desc()
        ).all()

    return render_template(
        "pages/student_registration.html",
        registrations=registrations,
        events=Event.query.order_by(Event.start_date).all(),
    )


@pages_bp.route("/portal/bookings")
@login_required(roles=[Role.ADMIN, Role.MANAGER, Role.ORGANIZER])
def bookings():
    return render_template("pages/bookings.html")


@pages_bp.route("/portal/evouchers")
@login_required(roles=[Role.ADMIN, Role.ORGANIZER, Role.STAFF])
def evoucher():
    return render_template("pages/evoucher.html")


@pages_bp.route("/portal/invoices")
@login_required(roles=[Role.ADMIN, Role.MANAGER])
def invoices():
    return render_template("pages/invoices.html")


@pages_bp.route("/portal/inbox")
@login_required(roles=[Role.ADMIN, Role.MANAGER, Role.STAFF])
def inbox():
    return render_template("pages/inbox.html")


@pages_bp.route("/portal/calendar")
@login_required()
def calendar():
    events = Event.query.order_by(Event.start_date).all()
    return render_template("pages/calendar.html", events=events)


@pages_bp.route("/portal/events/grid")
@login_required()
def events_grid():
    return render_template("pages/events_grid.html", events=Event.query.all())


@pages_bp.route("/portal/events/list")
@login_required()
def events_list():
    return render_template("pages/events_list.html", events=Event.query.all())


@pages_bp.route("/portal/events/<int:event_id>")
@login_required()
def event_details(event_id: int):
    event = Event.query.get_or_404(event_id)
    return render_template("pages/event_details.html", event=event)


@pages_bp.route("/portal/locations/<int:event_id>")
@login_required(roles=[Role.ADMIN, Role.MANAGER, Role.ORGANIZER])
def location_details(event_id: int):
    event = Event.query.get_or_404(event_id)
    return render_template("pages/location_details.html", event=event)


@pages_bp.route("/portal/financials")
@login_required(roles=[Role.ADMIN, Role.MANAGER])
def financials():
    total_revenue = db.session.query(db.func.sum(Event.revenue)).scalar() or 0
    total_registrations = Registration.query.count()
    return render_template(
        "pages/financial.html",
        total_revenue=total_revenue,
        total_registrations=total_registrations,
    )


@pages_bp.route("/portal/gallery")
@login_required()
def gallery():
    return render_template("pages/gallery.html", events=Event.query.all())


@pages_bp.route("/portal/feedback")
@login_required(roles=[Role.ADMIN, Role.MANAGER, Role.STAFF])
def feedback():
    sample_feedback = [
        {
            "author": "Sara Batool",
            "role": "Student Volunteer",
            "score": 4.8,
            "comment": "The Tech Summit logistics were stellar this year.",
            "submitted_at": datetime.utcnow(),
        },
        {
            "author": "Bilal Ahmed",
            "role": "Vendor Partner",
            "score": 4.2,
            "comment": "Great coordination, could improve booth allocations.",
            "submitted_at": datetime.utcnow(),
        },
    ]
    return render_template("pages/feedback.html", feedback=sample_feedback)

