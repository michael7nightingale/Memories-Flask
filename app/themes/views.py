import os

from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import login_required, current_user

from random import shuffle

from .repository import ThemeRepository, CardRepository
from app.utils import delete_images, generate_key, match_order

blueprint = Blueprint("themes", __name__, url_prefix='/themes', template_folder="templates", static_folder='static')


@blueprint.get('/<theme_id>',)
def theme_form_view_get(theme_id: str):
    """Separate theme view and testing logic."""
    cards = CardRepository().all_by_theme(theme_id)
    order = list(range(len(cards)))
    shuffle(order)
    ordered_cards = match_order(cards, order)
    response = make_response(
        render_template(
            'theme.html',
            cards=ordered_cards,
            theme=ThemeRepository().get(theme_id)
        )
    )
    response.set_cookie("order", "".join(str(i) for i in order))
    return response


@blueprint.post('/<theme_id>/')
def theme_form_view_post(theme_id):
    """Separate theme view and testing logic."""
    cards = CardRepository().all_by_theme(theme_id)
    cards = match_order(cards, map(int, request.cookies.get("order")))
    # right answers amount
    right_answers_amount = 0
    message = "<div>"
    form_data = request.form.to_dict()
    for i in range(len(cards)):
        answer = form_data.get(f"answer{i + 1}", "")
        if answer.lower().strip() == cards[i].answer.lower().strip():
            right_answers_amount += 1
        else:
            message += f"<h4 class='red_text'>{cards[i].question}: {answer} ({cards[i].answer})</h4>"

    if right_answers_amount == len(cards):
        message += "<h4 class='green_text'>Все верно!</h4></div>"
    else:
        message += "</div>"
    # form the html for flushing user what should he do
    result = f"Правильных ответов: {right_answers_amount} из {len(cards)}"
    if right_answers_amount == len(cards):
        advice = "<a href=\"{}\">Остальные темы</a>".format(request.cookies.get('url'))
    else:
        advice = "<a href=\"{}\">Попробовать снова</a>".format(url_for('.theme_form_view_get', theme_id=theme_id,))
    response = make_response(
        render_template(
            'results.html',
            result=result,
            advice=advice,
            theme_id=theme_id,
            message=message
        )
    )
    return response


@blueprint.route('/search/')
def search():
    """Searching themes by names."""
    if request.values:
        themes = ThemeRepository().find(request.form['substring'])
    else:
        themes = None
    response = make_response(
        render_template(
            "search.html",
            themes=themes,
        ),
    )
    response.set_cookie("url", request.url, 60*60)
    return response


@blueprint.post("/search/key/")
def search_key():
    try:
        theme = ThemeRepository().get_by(key=request.form['key'])
        return redirect(url_for("theme_form_view_get", title=theme.title, theme_id=theme.id))
    except Exception as e:
        print(e)
        return redirect(url_for("search"))


@blueprint.post("/delete/<theme_id>/")
def delete_theme(theme_id: str):
    theme = ThemeRepository().get(theme_id)
    if theme.user_id == current_user.id:
        ThemeRepository().delete(theme_id)
        delete_images(blueprint, current_user.id, theme_id)
        CardRepository().delete_by_theme(theme_id)
        return redirect(url_for("profileThemes", username=current_user.username))


@blueprint.get("/create-theme/")
@login_required
def get_create_theme():
    """Template view for create theme."""
    return render_template("create_theme.html")


@blueprint.post("/create-theme/")
@login_required
def post_create_theme():
    """Creating a new theme card"""
    form_data = request.form.to_dict()
    title = form_data['title']
    isPublic = bool(
        form_data.get("isPublic", False)
    )
    new_theme = ThemeRepository().create(
        title=title,
        isPublic=isPublic,
        key=generate_key(),
        user_id=current_user.id
    )
    theme_dir = blueprint.root_path + f"\\static\\images\\{current_user.id}\\{new_theme.id}"
    os.makedirs(theme_dir)
    count = form_data['count']
    for number in range(1, int(count) + 1):
        question = form_data[f'question{number}'].strip()
        answer = form_data[f'answer{number}'].strip().lower()
        image = request.files.get(f'photo{number}')
        static_path = None

        if image is not None:
            file_extension = image.filename.split('.')[-1]
            static_path = (
                    f'{current_user.id}\\{new_theme.id}\\{number}.{file_extension}'
            )
            image.filename = f"{number}.{file_extension}"
            full_path = blueprint.root_path + f"\\static\\images\\{static_path}"
            image.save(full_path)

        new_card = CardRepository().create(
            question=question,
            answer=answer,
            image=static_path,
            theme_id=new_theme.id
        )

    return redirect(url_for("profiles.get_profile_themes", username=current_user.username))
