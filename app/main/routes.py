from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.main.forms import EditProfileForm, CreateRoomForm
from app.models import User, Room
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    rooms = current_user.joined_rooms()
    return render_template('index.html', rooms=rooms)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        room = Room(name=form.name.data)
        db.session.add(room)
        current_user.join(room)
        db.session.commit()
        flash('Room created!')
        return redirect(url_for('main.index'))
    return render_template('create_room.html', title='Create a Room', form=form)
