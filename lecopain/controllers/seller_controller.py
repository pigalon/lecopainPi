from lecopain.dao.models import Seller
from lecopain.dao.seller_dao import SellerDao
from lecopain.services.seller_manager import SellerManager
from lecopain.app import app, db
from lecopain.form import SellerForm
from lecopain.helpers.pagination import Pagination
from flask import Blueprint, render_template, redirect, request, url_for, Flask, jsonify
from flask_login import login_required
from sqlalchemy.orm import load_only



app = Flask(__name__, instance_relative_config=True)


seller_page = Blueprint('seller_page', __name__,
                        template_folder='../templates')
sellerServices = SellerManager()


@seller_page.route("/sellers", methods=['GET', 'POST'])
@login_required
def sellers():
    sellers = SellerDao.get_all()
    return render_template('/sellers/sellers.html', sellers=sellers)


@seller_page.route("/sellers/new", methods=['GET', 'POST'])
@login_required
def create_seller():
    form = SellerForm()
    if form.validate_on_submit():
        seller = Seller(name=form.name.data, email=form.email.data, city=form.city.data)
        db.session.add(seller)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('seller_page.sellers'))
    return render_template('/sellers/create_seller.html', title='Ajouter un Vendeur', form=form)


@seller_page.route("/sellers/<int:seller_id>")
@login_required
def seller(seller_id):
    seller = sellerServices.get_one(seller_id)
    return render_template('/sellers/seller.html', seller=seller, title='Vendeur')


#####################################################################
#                                                                   #
#####################################################################
@seller_page.route("/sellers/update/<int:seller_id>", methods=['GET', 'POST'])
@login_required
def display_update_order(seller_id):
    seller = sellerServices.get_one(seller_id)
    form = SellerForm()

    if form.validate_on_submit():
        print('update form validate : ' + str(seller.id))

        #shipping_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.shipping_dt.data)
        seller.name = form.name.data
        seller.city = form.city.data
        seller.email = form.email.data

        db.session.commit()

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('seller_page.sellers'))
    else:
        form.name.data = seller.name
        form.city.data = seller.city
        form.email.data = seller.email

    return render_template('/sellers/update_seller.html', seller=seller, title='Mise a jour du vendeur', form=form)


#####################################################################
#                                                                   #
#####################################################################
@seller_page.route("/sellers/delete/<int:seller_id>")
@login_required
def display_delete_seller(seller_id):
    seller =sellerServices.get_one(seller_id)(seller_id)
    return render_template('/sellers/delete_seller.html', seller=seller, title='Suppression du vendeur')

#####################################################################
#                                                                   #
#####################################################################
@seller_page.route("/sellers/<int:seller_id>", methods=['DELETE'])
@login_required
def delete_seller(seller_id):
    seller = sellerServices.get_one(seller_id)
    db.session.delete(seller)
    db.session.commit()
    return jsonify({})

@seller_page.route('/api/sellers/')
@login_required
def api_sellers():
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10

    data, prev_page, next_page = sellerServices.optim_get_all_pagination(page=int(page), per_page=int(per_page))
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/sellers/',
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))
    
    
@seller_page.route("/api/sellers/<int:seller_id>")
@login_required
def api_seller(seller_id):
    return jsonify({'seller':sellerServices.read_one(seller_id)})
    

@seller_page.route('/api/sellers/select')
@login_required
def api_sellers_select():
    return jsonify({'sellers':sellerServices.optim_get_all()})
        
