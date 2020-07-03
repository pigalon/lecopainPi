from lecopain.app import app, db, login_manager
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, Flask, jsonify, request, flash, session
from werkzeug.urls import url_parse
from sqlalchemy.orm import load_only
from lecopain.form import LoginForm
from lecopain.form import UserForm
from lecopain.dao.models import User
from lecopain.dao.user_dao import UserDao
from lecopain.services.user_manager import userManager
from lecopain.services.role_manager import roleManager
from lecopain.helpers.pagination import Pagination

from flask_login import current_user, login_user
from flask_login import logout_user

from time import sleep




app = Flask(__name__, instance_relative_config=True)

user_page = Blueprint('user_page', __name__,
                      template_folder='../templates')

userServices = userManager()
roleServices = roleManager()


@user_page.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None: 
            app.logger.error(" fails not found authentication: " + str(form.username.data) +
                             " - " + str(form.password.data) +
                            " with IP address : " + str(request.remote_addr))
            flash("L'utilisateur n'existe pas !")
            sleep(3)
            return redirect(url_for('user_page.login'))
            
        if not user.check_password(form.password.data):
            flash("Le mot de passe est incorrect")
            sleep(3)
            app.logger.error(" fails authentication: " + str(form.username.data) +
                             " - " + str(form.password.data) +
                            " with IP address : " + str(request.remote_addr))

            return redirect(url_for('user_page.login'))

        login_user(user)

        return redirect(url_for('home'))

    else:
        return render_template('login.html', title='Se connecter', form=form)


@user_page.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_page.login'))


@user_page.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    users = userServices.optim_get_all()
    return render_template('/users/users.html', users=users)

@user_page.route("/users/new", methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = user(name=form.name.data, email=form.email.data, city=form.city.data)
        db.session.add(user)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('user_page.users'))
    return render_template('/users/create_user.html', title='Ajouter un Vendeur', form=form)


@user_page.route("/users/<int:user_id>")
@login_required
def user(user_id):
    user = userServices.get_one(user_id)
    return render_template('/users/user.html', user=user, title='Vendeur')


#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/update/<int:user_id>", methods=['GET', 'POST'])
@login_required
def display_update_order(user_id):
    user = user.query.get_or_404(user_id)
    form = UserForm()

    if form.validate_on_submit():
        print('update form validate : ' + str(user.id))

        #shipping_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.shipping_dt.data)
        user.name = form.name.data
        user.city = form.city.data
        user.email = form.email.data

        db.session.commit()

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('user_page.users'))
    else:
        form.name.data = user.name
        form.city.data = user.city
        form.email.data = user.email

    return render_template('/users/update_user.html', user=user, title='Mise a jour du vendeur', form=form)


#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/delete/<int:user_id>")
@login_required
def display_delete_user(user_id):
    user = user.query.get_or_404(user_id)
    return render_template('/users/delete_user.html', user=user, title='Suppression du vendeur')

#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/<int:user_id>", methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = user.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({})

@user_page.route('/api/users/roles/<string:role_name>')
@login_required
def api_users_by_role(role_name):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10

    data, prev_page, next_page = userServices.optim_get_all_pagination(role_name=role_name, page=int(page), per_page=int(per_page))
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/users/',
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

@user_page.route("/api/users/", methods=['GET', 'POST'])
@login_required
def api_users_all():
    return jsonify({'users': userServices.optim_get_all()})

@user_page.route("/api/users/roles", methods=['GET', 'POST'])
@login_required
def api_roles():
    return jsonify({'roles': roleServices.read_all()})


