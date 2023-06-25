from flask_migrate import Migrate

from app.app import create_app, db
from config import get_settings

FLASK_APP = "app"

app = create_app(get_settings())


if __name__ == '__main__':
    Migrate(app, db)
    app.run(debug=True)
