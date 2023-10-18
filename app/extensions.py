from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
socketio = SocketIO(cors_allowed_origins=['http://127.0.0.1:5000'])
