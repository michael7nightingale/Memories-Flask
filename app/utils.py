import os
import random

abc = [chr(__i) for __i in range(ord('a'), ord('z') + 1)] +\
      [chr(__i) for __i in range(ord('A'), ord('Z') + 1)] +\
      [',', '.', '-', ';', ':', '_']


def generate_key() -> str:
    key = "".join(random.choice(abc) for _ in range(30))
    return key


def delete_images(app, user_id: str, theme_id: str):
    theme_id = str(theme_id)
    path = app.root_path + f'/static/media/images/{user_id}/'
    files = [i for i in os.walk(path)][0][-1]
    for filename in files:
        if filename.split('_')[0] == theme_id:
            os.remove(path + filename)
