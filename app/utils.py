import os
import random
from typing import Iterable
from shutil import rmtree

abc = [chr(__i) for __i in range(ord('a'), ord('z') + 1)] +\
      [chr(__i) for __i in range(ord('A'), ord('Z') + 1)] +\
      [',', '.', '-', ';', ':', '_']


def generate_key() -> str:
    key = "".join(random.choice(abc) for _ in range(30))
    return key


def delete_theme(app, user_id: str, theme_id: str) -> None:
    path = app.root_path + f'/static/images/{user_id}/{theme_id}/'
    rmtree(path)


def match_order(lst: list, order: Iterable[int]) -> list:
    lst_ordered = []
    for idx in order:
        lst_ordered.append(lst[idx])
    return lst_ordered
