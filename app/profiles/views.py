from flask import Blueprint, render_template, make_response, request
from flask_login import login_required, current_user

from ..themes.repository import ThemeRepository
from app.users.repository import UserRepository


# initializing blueprint
blueprint = Blueprint(
    'profiles',
    __name__,
    # url_prefix="/profiles",
    template_folder="templates",
    static_folder='static',
)


@blueprint.get('/profile/<username>/')
@login_required
def profile(username: str):
    """User profile view"""
    user = UserRepository().get_by(username=username)
    if user == current_user:
        return render_template("self_profile.html",
                               user=current_user)
    else:
        ...


@blueprint.get('/profile/<username>/themes/')
@login_required
def get_profile_themes(username: str):
    """User themes view"""
    user = current_user
    themes = ThemeRepository().all_by_user(user.id)
    response = make_response(
        render_template(
            "themes.html",
            user=user,
            themes=themes
        )
    )
    response.set_cookie("url", request.url, 60 * 60)
    return response
