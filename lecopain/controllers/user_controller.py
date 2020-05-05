from lecopain.app import app, db, login_manager
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, Flask, jsonify, request, flash, session
from werkzeug.urls import url_parse
from sqlalchemy.orm import load_only
from lecopain.form import LoginForm
from lecopain.dao.models import User

from flask_login import current_user, login_user
from flask_login import logout_user

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, instance_relative_config=True)

user_page = Blueprint('user_page', __name__,
                      template_folder='../templates')


@user_page.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user_page.login'))

        login_user(user)

        return redirect(url_for('home'))

    else:
        return render_template('login.html', title='Sign In', form=form)


@user_page.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_page.login'))
