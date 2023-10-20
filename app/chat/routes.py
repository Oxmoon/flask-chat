from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send

from app import db, socketio
from app.chat import bp
from app.chat.forms import EditRoomForm
from app.models import Message, Room


@bp.route("/room/<name>", methods=["GET", "POST"])
@login_required
def room(name):
    room = Room.query.filter_by(name=name).first_or_404()
    avatar_url = current_user.get_avatar(50)
    return render_template(
        "chat/room.html",
        user=current_user,
        username=current_user.username,
        user_id=current_user.id,
        avatar_url=avatar_url,
        room=room,
        roomname=room.name,
        room_id=room.id,
        messages=room.messages,
    )


@bp.route("/room/edit_room/<name>", methods=["GET", "POST"])
@login_required
def edit_room(name):
    current_room = Room.query.filter_by(name=name).first_or_404()
    form = EditRoomForm(current_room.name)
    if not current_room.owner_id == current_user.id:
        flash("You do not have permission to edit this room.", "error")
        return redirect(url_for("chat.room", name=name))
    if form.validate_on_submit():
        current_room.name = form.name.data
        current_room.private = form.private.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("chat.room", name=form.name.data))
    elif request.method == "GET":
        form.name.data = current_room.name
        form.private.data = current_room.private
    return render_template(
        "chat/edit_room.html", title="Edit Room", current_room=current_room, form=form
    )


@bp.route("/room/delete/<name>", methods=["GET"])
@login_required
def delete_room(name):
    current_room = Room.query.filter_by(name=name).first_or_404()
    if not current_room.owner_id == current_user.id:
        flash("You do not have permission to delete this room.", "error")
        return redirect(url_for("chat.room", name=name))
    db.session.delete(current_room)
    db.session.commit()
    return redirect(url_for("main.index"))


@socketio.on("user_message")
def user_message(data):
    room = data["room_id"]
    message = Message(
        msg=data["msg"],
        user_id=data["user_id"],
        room_id=data["room_id"],
        avatar=data["avatar_url"],
        username=data["username"],
    )
    db.session.add(message)
    db.session.commit()
    send(
        {
            "msg": message.msg,
            "username": message.username,
            "timestamp": str(message.timestamp),
            "avatar_url": message.avatar,
        },
        room=room,
    )


@socketio.on("join")
def on_join(data):
    room = data["room_id"]
    print(current_user, "joined room", room)
    join_room(room)


@socketio.on("leave")
def on_leave(data):
    room = data["room_id"]
    print(current_user, "left room", room)
    leave_room(room)
