from __future__ import annotations

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from ..db import db
from ..models import User, Role
from .utils import login_user, logout_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get("next") or request.form.get("next") or url_for("pages.dashboard")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid credentials. Please try again.", "danger")
            return render_template("auth/login.html", next=next_url)

        if role and user.role.value != role:
            flash("You do not have access to that workspace.", "danger")
            return render_template("auth/login.html", next=next_url)

        login_user(user)
        flash(f"Welcome back, {user.full_name}!", "success")
        return redirect(next_url)

    return render_template("auth/login.html", next=next_url)


@auth_bp.route("/auth/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not all([full_name, email, password]):
            flash("All fields are required.", "warning")
            return render_template("auth/student_register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return render_template("auth/student_register.html")

        student = User(full_name=full_name, email=email, role=Role.STUDENT)
        student.set_password(password)
        db.session.add(student)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/student_register.html")


@auth_bp.route("/auth/logout")
def logout():
    logout_user()
    flash("Signed out successfully.", "info")
    return redirect(url_for("pages.landing"))

