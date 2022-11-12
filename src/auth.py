from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user
from src import db
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = db.get_user_by_username(username)
    if not user or not  check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('logged.profile'))

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    
    if db.check_username_in_use(username):
        flash('Username address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    
    db.add_user(new_user)
    
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
