from __future__ import annotations

from functools import wraps
from typing import Iterable

from flask import session, redirect, url_for, flash, g, abort, request

from ..models import User, Role


def get_current_user() -> User | None:
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return User.query.get(user_id)


def login_user(user: User) -> None:
    session["user_id"] = user.id
    session["role"] = user.role.value


def logout_user() -> None:
    session.pop("user_id", None)
    session.pop("role", None)


def login_required(roles: Iterable[Role | str] | None = None):
    required = {r.value if isinstance(r, Role) else r for r in roles or []}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if not user:
                flash("Please sign in to access that area.", "warning")
                next_url = request.path if request else url_for("pages.dashboard")
                return redirect(url_for("auth.login", next=next_url))
            if required and user.role.value not in required:
                abort(403)
            g.current_user = user
            return view(*args, **kwargs)

        return wrapped

    return decorator

