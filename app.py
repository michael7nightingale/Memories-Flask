from random import shuffle
from flask import Flask, url_for, render_template, request, flash, redirect, make_response
from flask_login import current_user, login_manager, LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import logging
import pydantic
import enum
import os
from werkzeug.security import generate_password_hash, check_password_hash

import validators
import utils

# ===============================CONFIGURATION================================= #
DATABASE = 'site.db'
DEBUG = True
SECRET_KEY = '123pasd;asdlamaf'

app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask458.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rammqueen'
db: SQLAlchemy = SQLAlchemy()
db.init_app(app)

# ----------------------------------LOGGING----------------------------------------#

logger = logging.Logger(name='app_loger', level='DEBUG')

file_handler = logging.FileHandler(filename='app.log')
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# -----------------------------------LOGIN-------------------------------------------#
loginManager = LoginManager(app)
loginManager.login_view = 'app.login'
loginManager.init_app(app)


@loginManager.user_loader
def loadUser(user_id):
    logger.debug(f"Loaded user with id: {user_id}")
    return Users.query.get(int(user_id))


# -----------------------------------DATABASE------------------------------------------#

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"{self.id=}, {self.username=}"


class Themes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    isPublic = db.Column(db.Boolean)
    key = db.Column(db.String(80), nullable=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.id=}, {self.title=}"


class TextCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ask_side = db.Column(db.Text)
    image = db.Column(db.String, nullable=True)
    answer_side = db.Column(db.String(255))
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))

    def __repr__(self):
        return f"{self.id=}, {self.ask_side=}"


def add_instance(model_instance):
    try:
        db.session.add(model_instance)
        db.session.flush()
        db.session.commit()
        return model_instance.id
    except Exception as e:
        logger.error(str(e))

# =====================================URLS==========================================#

@app.get('/')
def home():
    """Home page"""
    return render_template("index.html")


# --------------------------------USER-LOG-IN/OUT----------------------------------#

@app.route("/login/", methods=['GET', 'POST'])
def login():
    """Login user (by email)"""
    if request.method == "POST":
        try:
            user = db.session.query(Users).filter(Users.email == request.form['email']).first()
            logger.debug(f"User is taken from db query: {user}")
            if check_password_hash(user.password, request.form['password']):
                logger.debug("Password is checked with thw hashed one.")
                login_user(user, remember=True, force=True)
                logger.debug("Successfully logged in user.")
                return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Exception while logging user: {str(e)}")
            flash("Неверный email или пароль", category='status')
    # else if GET
    return render_template("login.html")


@app.route('/logout/', methods=['get', 'post'])
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for("home"))


def createUserModel(data: dict) -> pydantic.BaseModel:
    """Validating user data with pydantic"""
    try:
        userModel = validators.User(**data)
        return userModel
    except Exception as e:
        logger.error(f"Exception while creating user-model: {str(e)}")


@app.route('/register/', methods=['get', 'post'])
def register():
    """Register user"""
    if request.method == 'POST':
        try:
            # if any of input is not correct
            userModel = createUserModel(request.form.to_dict())
            logger.debug(f"User PyDantic model is created: {userModel}.")
            # password hashing
            passwordHash = generate_password_hash(request.form['password'])
            logger.debug("Password is hashed.")
            user = Users(password=passwordHash,
                         **userModel.dict(exclude={'password',}))
            logger.debug(f"User data is created by Model Users: {user}.")
            add_instance(user)
            logger.debug("User data is committed to db.")
            flash("Вы успешно зарегистрированы", category='status')
            os.makedirs(app.root_path + f'/static/media/images/{user.id}')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Exception while registering user: {str(e)}")
            flash("Ошибка при регистрации", category='status')
    # if form data is brilliant

    # if GET request or validation is failed
    return render_template("register.html")


# -----------------------------------PROFILE----------------------------------------#

@app.route('/profile/<username>/')
@login_required
def profile(username: str):
    """User profile view"""
    return render_template("profile/profile.html",
                           user=current_user)


@app.route('/profile/<username>/themes/')
@login_required
def profileThemes(username: str):
    """User profile view"""
    user = current_user
    themes = Themes.query.filter_by(user_id=user.id).all()
    response = make_response(
        render_template(
            "profile/themes.html",
            user=user,
            themes=themes
        )
    )
    print(request.url)
    response.set_cookie("url", request.url, 60 * 60)
    return response


# ----------------------------------THEME-CREATION---------------------------------------- #

@app.route("/create_theme/middleware/")
@login_required
def createThemeMiddleware():
    return render_template("profile/create_theme_middleware.html")


@app.route("/create_theme/", methods=['get', 'post'])
@login_required
def createTheme():
    print()
    """Creating a new theme card"""
    form_data = request.form.to_dict()
    form_data['number'] = int(form_data['number'])
    logger.debug(str(form_data))
    isPublic = request.form.get('isPublic', False)
    key = utils.generate_key()
    form_data['key'] = key

    return render_template("profile/create_theme.html", **form_data)


@app.post('/validate_theme/')
@login_required
def validateTheme():
    """Creating a new theme card"""
    try:
        isPublic = False if 'key' in request.form else True
        key = request.form['key']
        themeModel = validators.Theme(user_id=current_user.id,
                                      title=request.form['title'],
                                      isPublic=isPublic,
                                      key=key)
        logger.debug(f"Theme PyDantic model is created: {themeModel}.")
        theme = Themes(**themeModel.dict())
        logger.debug(f"Theme data is created by Model Theme: {theme}.")
        add_instance(theme)
        logger.debug("Theme data is committed to db.")
        logger.info(request.form)

        for i in range(1, int(request.form['number']) + 1):
            cardModel = validators.Card(theme_id=theme.id,
                                        ask_side=request.form[f'question{i}'],
                                        answer_side=request.form[f'answer{i}'])
            logger.debug(f"Card PyDantic model is created: {cardModel}.")
            image = request.files.get(f"image{i}", None)
            image_path = None
            if image:
                image_ext = image.filename.split('.')[-1]
                image_path = f'/{current_user.id}/{theme.id}_{i}.{image_ext}'
                image.save(app.root_path + f'/static/media/images/{image_path}')
            card = TextCard(**cardModel.dict(),
                            image=image_path
                            )
            logger.debug(f"Card data is created by Model Card: {card}.")
            add_instance(card)
            logger.debug("Card data is committed to db.")
        logger.debug("All cards of theme are added")
    except Exception as e:
        logger.error(f"Exception while creating theme-model: {str(e)}")
    # redirecting to all user themes
    return redirect(url_for('profileThemes', username=current_user.username))


@app.get('/<theme_id>/<title>/',)
def theme_form_view_get(theme_id: int, title: str):
    """Separate theme view and testing logic."""
    # if there were no recent prepare for the theme
    cooked_theme_id = request.cookies.get("theme_id", None)
    if cooked_theme_id is None:
        return redirect(url_for("theme_view", theme_id=theme_id))
    # common logic of theme-view
    cards = TextCard.query.filter_by(theme_id=theme_id).all()
    cards = [cards[int(i)] for i in request.cookies.get("order")]
    response = make_response(
        render_template(
            'themes/themes.html',
            cards=cards,
            title=title,
            theme_id=theme_id
            )
    )
    return response


@app.post('/<theme_id>/<title>/')
def theme_form_view_post(theme_id, title):
    """Separate theme view and testing logic."""
    print(request.cookies.get("order"))
    cards = TextCard.query.filter_by(theme_id=theme_id).all()
    cards = [cards[int(i)] for i in request.cookies.get("order")]
    # right answers amount
    right_answers_amount = sum(map(lambda x: int(x), (cards[i].answer_side == request.form[f"{i + 1}"] for i in range(len(cards)))))
    result = f"Правильных ответов: {right_answers_amount} из {len(cards)}"
    # form the html for flushing user what should he do
    if right_answers_amount == len(cards):
        advice = "<a href=\"{}\">Остальные темы</a>".format(request.cookies.get('url'))
    else:
        advice = "<a href=\"{}\">Попробовать снова</a>".format(url_for('theme_view',
                                                                           theme_id=theme_id,
                                                                           ))
    response = make_response(
        render_template(
            'themes/results.html',
            result=result,
            advice=advice,
            title=title,
            theme_id=theme_id
        )
    )
    return response


@app.get('/<theme_id>/prepare/')
def theme_view(theme_id: int):
    theme = Themes.query.filter_by(id=theme_id).first()
    cards_amount = TextCard.query.filter_by(theme_id=theme_id).count()
    order = list(range(cards_amount))
    shuffle(order)
    response = make_response(
        render_template(
            "themes/prepare.html",
            question_amount=cards_amount,
            title=theme.title,
            theme_id=theme_id
        )
    )
    response.set_cookie("theme_id", theme_id, 10)
    response.set_cookie("order", "".join((str(i) for i in order)), 3600)
    return response



# ===============================SEARCHING===============================#

@app.route('/search/')
def search():
    """Searching themes by names."""
    if request.values:
        logger.debug(f"Searching with {request.values}")
        query = Themes.query.filter(Themes.isPublic.is_(True)).filter(Themes.title.contains(request.values['substring'])).all()
    else:
        query = None
    response = make_response(
        render_template(
            "themes/search.html",
            themes=query,
        ),
    )
    print(request.url)
    response.set_cookie("url", request.url, 60*60)
    return response


@app.post("/search/key/")
def search_key():
    try:
        theme = Themes.query.filter_by(key=request.form['key']).first()
        return redirect(url_for("theme_form_view", title=theme.title, theme_id=theme.id))
    except Exception as e:
        logger.error(str(e))
        return redirect(url_for("search"))


@app.post("/delete/<theme_id>/")
def delete_theme(theme_id: int):
    theme = Themes.query.get(theme_id)
    if theme.user_id == current_user.id:
        db.session.delete(theme)
        delete_images(current_user.id, theme_id)
        db.session.commit()
        return redirect(url_for("profileThemes", username=current_user.username))

# ==============================================RUNNING============================================== #

def delete_images(user_id: int, theme_id: int):
    theme_id = str(theme_id)
    path = app.root_path + f'/static/media/images/{user_id}/'
    files = [i for i in os.walk(path)][0][-1]
    for filename in files:
        if filename.split('_')[0] == theme_id:
            os.remove(path + filename)



if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
