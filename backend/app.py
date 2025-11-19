from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from .config import Config
from .db import db
from .routes.utils import get_current_user

bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth import auth_bp
    from .routes.pages import pages_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def inject_user():
        return {"current_user": get_current_user()}

    @app.shell_context_processor
    def make_shell_context():
        from . import models

        return {"db": db, "models": models}

    return app


app = create_app()


if __name__ == "__main__":
    import os

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

