from flask import Flask

from pydantic import BaseSettings

from app.main.views import blueprint as main_blueprint
from app.users.views import blueprint as users_blueprint
from app.profiles.views import blueprint as profiles_blueprint
from app.themes.views import blueprint as themes_blueprint
from .extensions import db, login_manager


class Application:
    def __init__(self):
        self._app = Flask(__name__)

    def configure_app(self, settings: BaseSettings):
        self._app.config.from_object(settings)
        self._set_app_extensions()
        self._register_blueprints()
        self._configure_database()

    def _register_blueprints(self) -> None:
        self._app.register_blueprint(main_blueprint)
        self._app.register_blueprint(users_blueprint)
        self._app.register_blueprint(themes_blueprint)
        self._app.register_blueprint(profiles_blueprint, url_prefix='/profiles')

    def _set_app_extensions(self) -> None:
        db.init_app(self._app)
        login_manager.init_app(self._app)

    def _configure_database(self) -> None:
        @self._app.before_first_request
        def init_database():
            db.create_all()

        @self._app.teardown_request
        def shutdown_session(exception=None):
            db.session.remove()

    @property
    def app(self) -> Flask:
        return self._app    # type: ignore


def create_app(settings: BaseSettings) -> Flask:
    application = Application()
    application.configure_app(settings)
    return application.app
