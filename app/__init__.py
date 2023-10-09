from flask import Flask
from config import config
from sqlalchemy import MetaData, exc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import logging
from logging.handlers import RotatingFileHandler
import os

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
socketio = SocketIO(manage_session=False)


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
    app.register_blueprint(errors_bp, url_prefix='/errors')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        print("app.db already exists")
    else:
        print("app.db does not exist, will create ")
        with app.app_context():
            try:
                db.create_all()
            except exc.SQLAlchemyError as sqlalchemyerror:
                print("got the following SQLAlchemyError: " + str(sqlalchemyerror))
            except Exception as exception:
                print("got the following Exception: " + str(exception))
            finally:
                print("db.create_all() in __init__.py was successfull - no exceptions were raised")

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask-chat.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask-chat startup')

    return app
