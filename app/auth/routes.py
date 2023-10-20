from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, SignupForm
from app.models import Room, User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.identifier.data).first()
        if user is None:
            user = User.query.filter_by(email=form.identifier.data).first()
        if user is None:
            flash("Invalid email or username")
            return redirect(url_for("auth.login"))
        if not user.check_password(form.password.data):
            flash("Invalid password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        general_room = Room.query.filter_by(name="General").first()
        db.session.add(user)
        user.join(general_room)
        db.session.commit()
        flash("Thank you for signing up!")
        return redirect(url_for("auth.login"))
    return render_template("auth/sign_up.html", title="Sign up", form=form)
