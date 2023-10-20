from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Room, User


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Username already taken.")


class CreateRoomForm(FlaskForm):
    name = StringField("Room name", validators=[DataRequired()])
    private = BooleanField("Private Room")
    submit = SubmitField("Submit")

    def validate_name(self, name):
        room = Room.query.filter_by(name=self.name.data).first()
        if room is not None:
            raise ValidationError("Room name is already taken.")
