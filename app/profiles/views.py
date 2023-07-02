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
    if username == current_user.username:
        return render_template("self_profile.html")
    else:
        user = UserRepository().get_by(username=username)
        return render_template("profile.html", user=user)


@blueprint.get('/profile/<username>/themes/')
@login_required
def get_profile_themes(username: str):
    """User themes view"""
    if username == current_user.username:
        themes = ThemeRepository().all_by_user(current_user.id)
        response = make_response(
            render_template(
                "profile_themes_owner.html",
                themes=themes
            )
        )
        response.set_cookie("url", request.url, 60 * 60)
    else:
        user = UserRepository().get_by(username=username)
        themes = ThemeRepository().filter_by(user_id=user.id, isPublic=True)
        response = make_response(
            render_template(
                "profile_themes.html",
                user=user,
                themes=themes
            )
        )

    return response
