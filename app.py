from flask import Flask, url_for, render_template, g, current_app, request, flash, redirect, make_response
import flask_login
from flask_sqlalchemy import SQLAlchemy
import logging
import pydantic
import enum
from werkzeug.security import generate_password_hash, check_password_hash

import DataBaseSqlite  # my modules
import UserLogin
import validators
import utils


# ===============================CONFIGURATION================================= #
DATABASE = 'site.db'
DEBUG = True
SECRET_KEY = '123pasd;asdlamaf'

app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask45.db"
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
loginManager = flask_login.LoginManager(app)
loginManager.login_view = 'app.login'
loginManager.init_app(app)


@loginManager.user_loader
def loadUser(user_id):
    logger.debug(f"Loaded user with id: {user_id}")
    return Users.query.get(int(user_id))


# -----------------------------------DATABASE------------------------------------------#

class Users(db.Model, flask_login.UserMixin):
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
    key = db.Column(db.String(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.id=}, {self.title=}"


class TextCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)  # 1 - фото, 2 - текст
    ask_side = db.Column(db.Text)
    answer_side = db.Column(db.String(255))
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))

    def __repr__(self):
        return f"{self.id=}, {self.ask_side=}"


# =====================================URLS==========================================#

@app.get('/')
def home():
    """Home page"""
    return render_template("home.html")


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
                flask_login.login_user(user, remember=True, force=True)
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
    flask_login.logout_user()
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
            user = Users(password=passwordHash, **userModel.dict(exclude={'password',}))
            logger.debug(f"User data is created by Model Users: {user}.")
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            logger.debug("User data is committed to db.")
            flash("Вы успешно зарегистрированы", category='status')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Exception while registering user: {str(e)}")
            flash("Ошибка при регистрации", category='status')
    # if form data is brilliant

    # if GET request or validation is failed
    return render_template("register.html")


# -----------------------------------PROFILE----------------------------------------#

@app.route('/profile/<username>/')
@flask_login.login_required
def profile(username):
    """User profile view"""
    user = flask_login.current_user
    return render_template("profile/profile.html",
                           user=user)


@app.route('/profile/<username>/themes/')
@flask_login.login_required
def profileThemes(username):
    """User profile view"""
    user = flask_login.current_user
    themes = Themes.query.filter_by(user_id=user.id).all()
    return render_template("profile/themes.html",
                           user=user,
                           themes=themes)


@app.route('/create_theme/')
@flask_login.login_required
def createTheme():
    """Creating a new theme card"""
    # if request.method == 'POST':
    # print(request.form.keys())
    return render_template("profile/create_theme.html")


class Access(enum.Enum):
    PUBLIC = 'on'
    PRIVATE = 'off'

@app.post('/validate_theme/')
@flask_login.login_required
def validateCard():
    """Creating a new theme card"""
    try:
        themeModel = validators.Theme(user_id=flask_login.current_user.id,
                                      title=request.form['title'],
                                      isPublic=request.form.get('isPublic', False))
        logger.debug(f"Theme PyDantic model is created: {themeModel}.")
        if themeModel.isPublic:
            key = None
        else:
            key = utils.generate_key()
        theme = Themes(**themeModel.dict(exclude={'key', }),
                       key=key)
        logger.debug(f"Theme data is created by Model Theme: {theme}.")
        db.session.add(theme)
        db.session.flush()
        db.session.commit()
        logger.debug("Theme data is committed to db.")

        for i in range(1, 5):
            cardModel = validators.Card(theme_id=theme.id,
                                        type=2,
                                        ask_side=request.form[f'question{i}'],
                                        answer_side=request.form[f'answer{i}'])
            logger.debug(f"Card PyDantic model is created: {cardModel}.")
            card = TextCard(**cardModel.dict())
            logger.debug(f"Card data is created by Model Card: {card}.")
            db.session.add(card)
            db.session.flush()
            db.session.commit()
            logger.debug("Card data is committed to db.")
        logger.debug("All cards of theme are added")
    except Exception as e:
        logger.error(f"Exception while creating theme-model: {str(e)}")
    # redirecting to all user themes
    return redirect(url_for('profileThemes', username=flask_login.current_user.username))


@app.route('/<theme_id>/<title>')
def theme(theme_id, title):
    cards = TextCard.query.filter_by(theme_id=theme_id).all()
    response = make_response(render_template('themes/themes.html', cards=cards, title=title))
    response.headers['Content-Type'] = "text/html"
    for i, card in enumerate(cards, 1):
        response.set_cookie(str(i), card.answer_side, 60*60)
    return response


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
