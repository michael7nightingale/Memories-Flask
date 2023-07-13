from flask_migrate import Migrate
from flask import Flask

from app.app import create_app, db
from config import get_settings


app: Flask = create_app(get_settings())


if __name__ == '__main__':
    Migrate(app, db)
    app.run()
