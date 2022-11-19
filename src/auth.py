from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import Response

from src import db
from src.models.kinks import Kinks
from src.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login() -> str:
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post() -> Response:
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = db.get_user_by_username(username)
    if not user or not password or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("logged.profile"))


@auth.route("/signup")
def signup() -> str:
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post() -> Response:
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    if db.check_username_in_use(username):
        flash("Username address already exists")
        return redirect(url_for("auth.signup"))

    if not password:
        flash("Password is required")
        return redirect(url_for("auth.signup"))

    if not username:
        flash("Username is required")
        return redirect(url_for("auth.signup"))

    new_user = User(
        email=email,
        username=username,
        password=generate_password_hash(password, method="sha256"),
        kinks=Kinks(sub=[], dom=[]),
    )

    db.add_user(new_user)

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for("main.index"))
