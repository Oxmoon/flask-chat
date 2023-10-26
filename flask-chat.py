import os

from flask_migrate import Migrate

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
    print("deploy was called!")
    db.create_all()
    print("db created")
    # ensure general room is created
    general_room = Room.query.filter_by(name="General").first()
    print(general_room)
    if general_room is None:
        print("no General room")
        general_room = Room(name="General", private=False, owner_id=None)
        db.session.add(general_room)
        db.session.commit()
