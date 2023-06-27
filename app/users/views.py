import os

from flask import Blueprint, request, flash, render_template, redirect, url_for
from app.themes.views import blueprint as themes_blueprint
from flask_login import logout_user, login_user

from app import schemas
from .repository import UserRepository
from app.extensions import login_manager, add_instance


@login_manager.user_loader
def load_user(user_id):
    return UserRepository().get(user_id)


blueprint = Blueprint("users", __name__, url_prefix='/auth', template_folder="templates", static_folder='static')


@blueprint.route("/login/", methods=['GET', 'POST'])
def login():
    """Login user (by email)"""
    if request.method == "POST":
        try:
            print(request.form.to_dict())
            user = UserRepository().login(request.form['email'], request.form['password'])
            print(user)
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
            add_instance(user)
            flash("Вы успешно зарегистрированы", category='status')
            os.makedirs(themes_blueprint.root_path + f'/static/images/{user.id}')
            return redirect(url_for('users.login'))
        except Exception as e:
            print(e)
            flash("Ошибка при регистрации", category='status')
    # if form data is brilliant

    # if GET request or validation is failed
    return render_template("register.html")
