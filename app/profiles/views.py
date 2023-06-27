from flask import Blueprint, render_template, make_response, request
from flask_login import login_required, current_user

from ..themes.repository import ThemeRepository
from ..utils import generate_key

blueprint = Blueprint('profiles', __name__, url_prefix="/profiles", template_folder="templates", static_folder='static')


@blueprint.route('/profile/<username>/')
@login_required
def profile(username: str):
    """User profile view"""
    return render_template("profile.html",
                           user=current_user)


@blueprint.route("/create_theme/middleware/")
@login_required
def createThemeMiddleware():
    return render_template("create_theme_middleware.html")


@blueprint.route("/create_theme/", methods=['get', 'post'])
@login_required
def createTheme():
    """Creating a new theme card"""
    form_data = request.form.to_dict()
    form_data['number'] = int(form_data['number'])  # type: ignore
    # isPublic = request.form.get('isPublic', False)
    key = generate_key()
    form_data['key'] = key
    return render_template("create_theme.html", **form_data)


@blueprint.route('/profile/<username>/themes/')
@login_required
def profileThemes(username: str):
    """User profile view"""
    user = current_user
    themes = ThemeRepository().all_by_user(user.id)
    print(themes)
    response = make_response(
        render_template(
            "themes.html",
            user=user,
            themes=themes
        )
    )
    response.set_cookie("url", request.url, 60 * 60)
    return response
