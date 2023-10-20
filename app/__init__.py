from flask import Flask

from config import config

from .extensions import bootstrap, db, login, migrate, moment, socketio


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    socketio.init_app(app)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp, url_prefix="/errors")

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.chat import bp as chat_bp

    app.register_blueprint(chat_bp, url_prefix="/chat")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
