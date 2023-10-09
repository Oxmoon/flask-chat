import os
from app import create_app, db
from app.models import User, Message, Room
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

with app.app_context():
    general_room = Room.query.filter_by(name="General").first()
    if general_room is None:
        general_room = Room(name="General",
                            private=False)
        db.session.add(general_room)
        db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message, 'Room': Room}
