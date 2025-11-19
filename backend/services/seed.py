from __future__ import annotations

from datetime import date

from ..app import create_app
from ..db import db
from ..models import User, Role, Event


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@ventixe.io").first():
            admin = User(full_name="Super Admin", email="admin@ventixe.io", role=Role.ADMIN)
            admin.set_password("Admin@123")
            db.session.add(admin)

        if not Event.query.first():
            events = [
                Event(
                    title="UOS Annual Tech Summit",
                    category="Technology",
                    location="Main Auditorium",
                    capacity=2000,
                    start_date=date(2025, 10, 20),
                    status="active",
                    revenue=1800000,
                ),
                Event(
                    title="Intra-University Cricket Tournament",
                    category="Sports",
                    location="Sports Complex",
                    capacity=32,
                    start_date=date(2025, 11, 5),
                    status="completed",
                    revenue=620000,
                ),
                Event(
                    title="Arts & Culture Day",
                    category="Culture",
                    location="Open-Air Theatre",
                    capacity=1000,
                    start_date=date(2025, 12, 1),
                    status="planned",
                    revenue=250000,
                ),
            ]
            db.session.add_all(events)

        db.session.commit()
        print("Database seeded.")


if __name__ == "__main__":
    seed()

