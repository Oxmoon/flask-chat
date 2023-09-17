from app import db, socketio
from app.chat import bp
from app.models import User, Room
from app.chat.forms import ChatForm
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send


@bp.route('/room/<name>', methods=['GET', 'POST'])
@login_required
def room(name):
    form = ChatForm()
    room = Room.query.filter_by(name=name).first_or_404()
    return render_template('chat/room.html', room=room, form=form)


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send(data)
