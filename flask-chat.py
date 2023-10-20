import os

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import Message, Room, User, user_room

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Message": Message,
        "Room": Room,
        "user_room": user_room,
    }


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    upgrade()
