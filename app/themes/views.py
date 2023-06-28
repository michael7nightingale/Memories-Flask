from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import login_required, current_user

from random import shuffle

from .repository import ThemeRepository, CardRepository
from app.extensions import add_instance
from app import schemas
from app.utils import delete_images, generate_key

blueprint = Blueprint("themes", __name__, url_prefix='/themes', template_folder="templates", static_folder='static')


@blueprint.post('/validate-theme/')
@login_required
def validateTheme():
    """Creating a new theme card"""
    try:
        isPublic = False if 'key' in request.form else True
        key = request.form['key']
        themeModel = schemas.Theme(
            user_id=current_user.id,
            title=request.form['title'],
            isPublic=isPublic,
            key=key
        )
        theme = ThemeRepository().create(**themeModel.dict())
        add_instance(theme)

        for i in range(1, int(request.form['number']) + 1):
            cardModel = schemas.Card(theme_id=theme.id,
                                     ask_side=request.form[f'question{i}'],
                                     answer_side=request.form[f'answer{i}'])
            image = request.files.get(f"image{i}", None)
            image_path = None
            if image:
                image_ext = image.filename.split('.')[-1]
                image_path = f'/{current_user.id}/{theme.id}_{i}.{image_ext}'
                image.save(blueprint.root_path + f'/static/media/images/{image_path}')
            CardRepository().create(**cardModel.dict(), image=image_path)   # type: ignore
    except Exception as e:
        print(e)
    # redirecting to all user themes
    return redirect(url_for('profiles.profileThemes', username=current_user.username))


@blueprint.get('/<theme_id>/<title>/',)
def theme_form_view_get(theme_id: str, title: str):
    """Separate theme view and testing logic."""
    # if there were no recent prepare for the theme
    cooked_theme_id = request.cookies.get("theme_id"),
    order = request.cookies.get("order")
    if cooked_theme_id is None or order is None:
        return redirect(url_for("theme_view", theme_id=theme_id))
    # common logic of theme-view
    cards = CardRepository().all_by_theme(theme_id)
    cards = [cards[int(i)] for i in order]

    response = make_response(
        render_template(
            'themes.html',
            cards=cards,
            title=title,
            theme_id=theme_id
            )
    )
    return response


@blueprint.post('/<theme_id>/<title>/')
def theme_form_view_post(theme_id, title):
    """Separate theme view and testing logic."""
    cards = CardRepository().all_by_theme(theme_id)
    cards = [cards[int(i)] for i in request.cookies.get("order")]
    # right answers amount
    right_answers_amount = 0
    message = "<div>"
    for i in range(len(cards)):
        answer = request.form[f"{i + 1}"]
        if answer.lower().strip() == cards[i].answer_side.lower().strip():
            right_answers_amount += 1
        else:
            message += f"<h4 class='red_text'>{cards[i].ask_side}: {answer} ({cards[i].answer_side})</h4>"

    if right_answers_amount == len(cards):
        message += "<h4 class='green_text'>Все верно!</h4></div>"
    else:
        message += "</div>"
    # form the html for flushing user what should he do
    result = f"Правильных ответов: {right_answers_amount} из {len(cards)}"
    if right_answers_amount == len(cards):
        advice = "<a href=\"{}\">Остальные темы</a>".format(request.cookies.get('url'))
    else:
        advice = "<a href=\"{}\">Попробовать снова</a>".format(url_for('theme_view', theme_id=theme_id,))
    response = make_response(
        render_template(
            'results.html',
            result=result,
            advice=advice,
            title=title,
            theme_id=theme_id,
            message=message
        )
    )
    return response


@blueprint.get('/<theme_id>/prepare/')
def theme_view(theme_id: str):
    theme = ThemeRepository().get(theme_id)
    cards_amount = CardRepository().count_by_theme(theme_id)
    order = list(range(cards_amount))
    shuffle(order)
    response = make_response(
        render_template(
            "prepare.html",
            question_amount=cards_amount,
            title=theme.title,
            theme_id=theme_id
        )
    )
    response.set_cookie("theme_id", str(theme_id), 5)
    response.set_cookie("order", "".join((str(i) for i in order)), 3600)
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



    form_data['number'] = int(form_data['number'])  # type: ignore
    isPublic = request.form.get('isPublic', False)

    key = generate_key()
    form_data['key'] = key
    return render_template("create_theme.html", **form_data)
