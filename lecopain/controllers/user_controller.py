from lecopain import app, db, login_manager
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

#@user_page.route('/login', methods=['POST'])
#def do_admin_login():

#    user = User.query.filter_by(username = request.form['username']).first()
    
#    if user is None or not check_password_hash( user.password, request.form['password']):
#        flash('Invalid username or password')
#    else:
#        session['logged_in'] = True 
#    return redirect(url_for('home'))


@user_page.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    print('login' + request.method)
    #if current_user.is_authenticated:
    if form.validate_on_submit():
        print('login validate')
        user = User.query.filter_by(username=form.username.data).first()
        
        print('u : ' + str(user.id) + str(user.password) + " -  " + str(form.password.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #login_user(user, remember=form.remember_me.data)
        login_user(user)
        #return redirect(url_for('index'))
        return redirect(url_for('home'))
        
    else :
        print('login no val')

        return render_template('login.html', title='Sign In', form=form)
    


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     print("!!!!!! form")
#     form = LoginForm()
#     if form.validate_on_submit():
#         print("!!!!!! validate")
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)

#         flask.flash('Logged in successfully.')

#         #next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         if not is_safe_url(next):
#             return flask.abort(400)
#         return redirect(url_for('home'))
#         #return flask.redirect(next or flask.url_for('home'))
#         print("!!!!!! not")
#     return flask.render_template('login.html', form=form)

#@login.user_loader
#def load_user(user_id):
#    return User.get(user_id)

@user_page.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_page.login'))

