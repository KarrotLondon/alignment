import os
from dotenv import dotenv_values
from flask import Flask
from flask_login import LoginManager
from src.wrappers.mongo import Mongo
from src.kink_lists.kink_list import get_kinks

config = dotenv_values(".env")

value = os.environ.get("ATLAS_URI") if os.environ.get("ATLAS_URI") else config["ATLAS_URI"]

db = Mongo(value)
kink_list = get_kinks()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
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