from app import db, socketio
from app.chat import bp
from app.models import User, Room, Message
from app.chat.forms import ChatForm
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send, emit


@bp.route('/room/<name>', methods=['GET', 'POST'])
@login_required
def room(name):
    room = Room.query.filter_by(name=name).first_or_404()
    return render_template('chat/room.html',
                           user=current_user,
                           username=current_user.username,
                           user_id=current_user.id,
                           room=room,
                           roomname=room.name,
                           room_id=room.id,
                           messages=room.messages)


@socketio.on('message')
def message(data):
    print(f"\n\n{data['msg']}\n\n")
    send(data)


@socketio.on('user_message')
def user_message(data):
    message = Message(msg=data['msg'],
                      user_id=data['user_id'],
                      room_id=data['room_id'])
    db.session.add(message)
    db.session.commit()
    emit("display_message", {"msg": message.msg,
                             "username": data['username'],
                             "timestamp": str(message.timestamp)})
