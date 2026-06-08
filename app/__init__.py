import os
from datetime import datetime
from flask import Flask
from config import config
from app.extensions import db, mail, csrf


def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from app.public import public_bp
    from app.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.jinja_env.globals["current_year"] = lambda: datetime.utcnow().year

    return app
