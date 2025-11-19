from __future__ import annotations

from flask import Blueprint, request, jsonify

from ..db import db, get_db
from ..models import Registration, Event, Role
from .utils import login_required

api_bp = Blueprint("api", __name__)


@api_bp.route("/registrations", methods=["POST"])
def create_registration():
    data = request.get_json() or {}
    required = ["student_name", "student_id", "email", "event_id"]
    if not all(key in data and data[key] for key in required):
        return jsonify({"error": "Missing required fields"}), 400

    event = Event.query.get(data["event_id"])
    if not event:
        return jsonify({"error": "Event not found"}), 404

    registration = Registration(
        student_name=data["student_name"],
        student_id=data["student_id"],
        email=data["email"],
        phone=data.get("phone"),
        department=data.get("department"),
        status="pending",
        event_id=event.id,
    )
    db.session.add(registration)
    db.session.commit()
    return jsonify({"message": "Registration submitted", "id": registration.id}), 201


@api_bp.route("/registrations", methods=["GET"])
@login_required(roles=[Role.ADMIN, Role.MANAGER, Role.ORGANIZER, Role.STAFF])
def list_registrations():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()
    payload = [
        {
            "id": reg.id,
            "student_name": reg.student_name,
            "event": reg.event.title,
            "status": reg.status,
            "created_at": reg.created_at.isoformat(),
        }
        for reg in registrations
    ]
    return jsonify(payload)


@api_bp.route("/external/events", methods=["GET"])
def remote_events():
    """Fetch events from the InfinityFree MySQL database via PyMySQL."""
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events")
            rows = cursor.fetchall()
    finally:
        conn.close()
    return jsonify(rows)


@api_bp.route("/external/events", methods=["POST"])
@login_required(roles=[Role.ADMIN, Role.MANAGER])
def remote_add_event():
    """Insert an event record into the InfinityFree MySQL database."""
    payload = request.get_json() or {}
    title = payload.get("title")
    date_value = payload.get("date")
    if not title or not date_value:
        return jsonify({"error": "Both 'title' and 'date' are required."}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO events (title, date) VALUES (%s, %s)",
                (title, date_value),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"message": "Event added successfully."}), 201

