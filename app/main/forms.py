from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User, Room


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username already taken.')


class CreateRoomForm(FlaskForm):
    name = StringField('Room name', validators=[DataRequired()])
    private = BooleanField('Private Room')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        room = Room.query.filter_by(name=self.name.data).first()
        if room is not None:
            raise ValidationError('Room name is already taken.')


class InviteToRoomForm(FlaskForm):
    room_name = StringField('Room name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(InviteToRoomForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_name(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            raise ValidationError('This user does not exist.')

    def validate_room(self, user):
        this_user = User.query.filter_by(username=self.user).first()
        room = Room.query.filter_by(name=self.room_name.data).first()
        if room not in this_user.joined_rooms():
            raise ValidationError('You have not joined this room.')
