import random

abc = [chr(__i) for __i in range(ord('a'), ord('z') + 1)] +\
      [chr(__i) for __i in range(ord('A'), ord('Z') + 1)] +\
      [',', '.', '-', ';', ':', '_']


def generate_key() -> str:
    key = "".join(random.choice(abc) for _ in range(30))
    return key



