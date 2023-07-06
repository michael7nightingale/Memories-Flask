import os

from flask import Blueprint, request, flash, render_template, redirect, url_for
from app.themes.views import blueprint as themes_blueprint
from flask_login import logout_user, login_user

from app import schemas
from .repository import UserRepository
from app.extensions import login_manager, add_instance
from .tokens import confirm_token, generate_token
from app.emails import send_message


@login_manager.user_loader
def load_user(user_id):
    return UserRepository().get(user_id)


blueprint = Blueprint("users", __name__, url_prefix='/auth', template_folder="templates", static_folder='static')


def send_email_activation(user) -> None:
    """ Generate and send activation link to email."""
    token = generate_token(email=user.email)
    link = request.host_url + blueprint.url_prefix + f"/{user.id}/" + token
    message = f"""Finish registration by following the link:
                {link}"""
    send_message(
        to_addrs=[user.email],
        subject="User activation.",
        body=message
    )


@blueprint.route("/login/", methods=['GET', 'POST'])
def login():
    """Login user (by email)"""
    if request.method == "POST":
        try:
            user = UserRepository().login(request.form['email'], request.form['password'])
            if user is not None:
                login_user(user, remember=True, force=True)
                return redirect(url_for('main.homepage'))
            else:
                flash("Неправильные данные")
        except Exception as e:
            print(e)
            flash("Неверный email или пароль", category='status')
    # else if GET
    return render_template("login.html")


@blueprint.route('/logout/', methods=['get', 'post'])
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for("main.homepage"))


@blueprint.route('/register/', methods=['get', 'post'])
def register():
    """Register user"""
    if request.method == 'POST':
        try:
            # if any of input is not correct
            user_schema = schemas.User(**request.form.to_dict())
            # password hashing
            user = UserRepository().register(**user_schema.dict())
            send_email_activation(user)
            flash("Activation link is sent to your email. Please, confirm you account.")
            return redirect(url_for('main.homepage'))
        except Exception as e:
            print(e)
            flash("Ошибка при регистрации", category='status')
    # if form data is brilliant

    # if GET request or validation is failed
    return render_template("register.html")


@blueprint.get("/<uid>/<token>/")
def activate_user(uid, token):
    """Endpoint of activating user by following the link"""
    user = UserRepository().get(uid)
    email = confirm_token(token=token)
    if email and user.email == email and not user._is_active:
        user._is_active = True
        add_instance(user)
        os.makedirs(themes_blueprint.root_path + f'/static/images/{user.id}')
        return redirect(url_for('users.login'))

    return redirect(url_for("main.homepage"))

