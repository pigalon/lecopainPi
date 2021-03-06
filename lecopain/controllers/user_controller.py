from lecopain.app import app, db, login_manager
from flask import Blueprint, render_template, redirect, url_for, Flask, jsonify, request, flash, session
from werkzeug.urls import url_parse
from sqlalchemy.orm import load_only
from lecopain.form import LoginForm
from lecopain.form import UserForm, PasswordForm
from lecopain.dao.models import User, UserRoles, Role
from lecopain.dao.user_dao import UserDao
from lecopain.services.user_manager import UserManager
from lecopain.services.role_manager import roleManager
from lecopain.helpers.pagination import Pagination

from flask_login import (current_user, 
                        login_required, 
                        logout_user, 
                        login_user)

from lecopain.helpers.roles_utils import admin_login_required

from time import sleep


app = Flask(__name__, instance_relative_config=True)

user_page = Blueprint('user_page', __name__,
                    template_folder='../templates')

userServices = UserManager()
roleServices = roleManager()


@user_page.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        
        user = userServices.get_by_username(username=form.username.data)

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
        #admin
        if user.get_main_role() == 'admin_role':
            return redirect(url_for('home'))
        elif user.get_main_role() == 'customer_role':
            return redirect(url_for('customer_main_page.home'))
        elif user.get_main_role() == 'seller_role':
            return redirect(url_for('seller_main_page.home'))
        # simple user

    else:
        return render_template('login.html', title='Se connecter', form=form)
    


@user_page.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_page.login'))


@user_page.route("/users", methods=['GET', 'POST'])
@login_required
@admin_login_required
def users():
    users = userServices.optim_get_all()
    return render_template('/users/users.html', users=users)


@user_page.route("/users/new", methods=['GET', 'POST'])
@login_required
@admin_login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        if userServices.login_already_used(form.username.data):
            flash(f'Login déjà utilisé : {form.username.data}!', 'error')
        else:                
            userServices.create(form)
            #flash(f'People created for {form.firstname.data}!', 'success')
            return redirect(url_for('user_page.users'))
    else :
        flash_errors(form)
    roles = roleServices.get_all()
    return render_template('/users/create_user.html', title='Ajouter un Utilisateur', roles=roles, form=form)

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u" %s : %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')



@user_page.route("/users/<int:user_id>")
@login_required
@admin_login_required
def user(user_id):
    user = userServices.get_one(user_id)
    return render_template('/users/user.html', user=user, title='Utilisateur')


#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/update/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def update_user(user_id):
    user = userServices.get_one(user_id)
    form = UserForm()

    if form.validate_on_submit():
        userServices.update(user, form)
        
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(f'/users/{user_id}')
    else:
        form.username.data = user.username
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.email.data = user.email
    roles = roleServices.get_all()
    return render_template('/users/update_user.html', user=user, roles=roles, title='Mise a jour de l\'utilisateur', form=form)

#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/update/<int:user_id>/password", methods=['GET', 'POST'])
@login_required
@admin_login_required
def update_password(user_id):
    
    form = PasswordForm()

    if form.validate_on_submit():
        
        userServices.change_password(user_id, form.password.data)
        return redirect(f'/users/{user_id}')
    
    return render_template('/users/update_password.html', user=user, title='Mise à jour du mot de passe', form=form)


#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/update/<int:user_id>/role", methods=['GET', 'POST'])
@login_required
@admin_login_required
def update_role(user_id):
    return render_template('/users/update_role.html', user_id=user_id, title='Mise à jour du role et compte associé')


@user_page.route("/users/<int:user_id>/active", methods=['GET', 'POST'])
@login_required
@admin_login_required
def active_user(user_id):
    userServices.active(user_id)
    return redirect(f'/users/{user_id}')

@user_page.route("/users/<int:user_id>/deactivate", methods=['GET', 'POST'])
@login_required
@admin_login_required
def deactivate_user(user_id):
    userServices.deactivate(user_id)
    return redirect(f'/users/{user_id}')



#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/delete/<int:user_id>")
@login_required
@admin_login_required
def display_delete_user(user_id):
    user = userServices.get_one(user_id)
    return render_template('/users/delete_user.html', user=user, title='Suppression de l\'utilisateur')

#####################################################################
#                                                                   #
#####################################################################
@user_page.route("/users/<int:user_id>", methods=['DELETE'])
@login_required
@admin_login_required
def delete_user(user_id):
    userServices.delete(user_id)
    return jsonify({})

@user_page.route('/api/users/roles/<string:role_id>')
@login_required
@admin_login_required
def api_users_by_role(role_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10

    data, prev_page, next_page = userServices.optim_get_all_pagination(
        role_id=int(role_id), page=int(page), per_page=int(per_page))
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/users/roles/'+role_id,
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

@user_page.route("/api/users/", methods=['GET', 'POST'])
@login_required
@admin_login_required
def api_users_all():
    return jsonify({'users': userServices.optim_get_all()})

@user_page.route("/api/users/roles", methods=['GET', 'POST'])
@login_required
@admin_login_required
def api_roles():
    return jsonify({'roles': roleServices.read_all()})

@user_page.route("/api/users/update/<int:user_id>/role/<int:role_id>/account/<int:account_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def api_change_role(user_id, role_id, account_id):
    role = roleServices.get_one(role_id)
    userServices.change_role(user_id, role, account_id)
    return jsonify({})

@user_page.route("/api/users/<int:user_id>")
@login_required
@admin_login_required
def api_user(user_id):
    return jsonify({'user':userServices.read_one(user_id)})




