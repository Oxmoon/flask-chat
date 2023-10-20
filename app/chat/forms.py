from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import Room


class ChatForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


class EditRoomForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    private = BooleanField("Private")
    submit = SubmitField("Send")

    def __init__(self, original_name, *args, **kwargs):
        super(EditRoomForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            room = Room.query.filter_by(name=self.name.data).first()
            if room is not None:
                raise ValidationError("Room name is already taken.")
