import os
from typing import Optional, cast

from dotenv import dotenv_values
from flask import Flask
from flask_login import LoginManager

from src.kink_lists.kink_list import get_kinks
from src.models.user import User
from src.wrappers.mongo import MongoWrapper

config = dotenv_values(".env")

value = cast(str, os.environ.get("ATLAS_URI") if os.environ.get("ATLAS_URI") else config["ATLAS_URI"])

db = MongoWrapper(value)
kink_list = get_kinks()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "super secret key"

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        return db.get_user_by_id(user_id)

    # blueprint for auth routes in our app
    from src.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from src.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from src.logged_in import logged as logged_in_blueprint

    app.register_blueprint(logged_in_blueprint)

    return app
