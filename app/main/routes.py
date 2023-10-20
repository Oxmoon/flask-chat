from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import CreateRoomForm, EditProfileForm
from app.models import Room, User


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    rooms = current_user.joined_rooms()
    return render_template("index.html", rooms=rooms)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template("user.html", user=user)


@bp.route("/user/<username>/invite_room", methods=["GET", "POST"])
@login_required
def invite_room(username):
    user = User.query.filter_by(username=username).first_or_404()
    rooms = current_user.invitable_rooms(user)
    if request.method == "POST":
        room_id = request.form["room_button"]
        room = Room.query.filter_by(id=room_id).first_or_404()
        user.join(room)
        db.session.commit()
        flash(user.username + " has been invited to " + room.name + ".")
    return render_template(
        "invite_room.html", title="Invite to Room", user=user, rooms=rooms
    )


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))
    if request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@bp.route("/create_room", methods=["GET", "POST"])
@login_required
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        room = Room(
            name=form.name.data, private=form.private.data, owner_id=current_user.id
        )
        db.session.add(room)
        current_user.join(room)
        db.session.commit()
        flash("Room created!")
        return redirect(url_for("main.index"))
    return render_template("create_room.html", title="Create a Room", form=form)
