from lecopain.models import Vendor
from lecopain.services.vendor_manager import VendorManager
from lecopain import app, db
from lecopain.form import VendorForm
from flask import Blueprint, render_template, redirect, url_for, Flask, jsonify
from sqlalchemy.orm import load_only


app = Flask(__name__, instance_relative_config=True)


vendor_page = Blueprint('vendor_page', __name__,
                        template_folder='../templates')

@vendor_page.route("/vendors", methods=['GET', 'POST'])
def vendors():
    new_orders=[]
    vendorManager = VendorManager()
    vendors = Vendor.query.all()
    for vendor in vendors :
        new_orders.append(vendorManager.get_last_order(vendor))
    for order in new_orders :
        if order != None :
            print(str(order.order_dt))
    return render_template('/vendors/vendors.html', vendors=vendors, new_orders= new_orders, cpt=0)

@vendor_page.route("/vendors/new", methods=['GET', 'POST'])
def create_vendor():
    form = VendorForm()
    if form.validate_on_submit():
        vendor = Vendor(name=form.name.data, email=form.email.data)
        db.session.add(vendor)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('vendor_page.vendors'))
    return render_template('/vendors/create_vendor.html', title='Formulaire Vendeur', form=form)

@vendor_page.route("/vendors/<int:vendor_id>")
def vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    return render_template('/vendors/vendor.html', vendor=vendor)

#####################################################################
#                                                                   #
#####################################################################
@vendor_page.route("/vendors/update/<int:vendor_id>", methods=['GET', 'POST'])
def display_update_order(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    form = VendorForm()

    if form.validate_on_submit():
        print('update form validate : ' + str(vendor.id))

        #order_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.order_dt.data)
        vendor.name = form.name.data
        vendor.email=form.email.data

        db.session.commit()
        
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('vendor_page.vendors'))
    else:
        form.name.data = vendor.name
        form.email.data = vendor.email
        

    return render_template('/vendors/update_vendor.html', vendor=vendor, title='Mise a jour de vendeur', form=form)


#####################################################################
#                                                                   #
#####################################################################
@vendor_page.route("/vendors/delete/<int:vendor_id>")
def display_delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    return render_template('/vendors/delete_vendor.html', vendor=vendor, title='Suppression de vendeur')

#####################################################################
#                                                                   #
#####################################################################
@vendor_page.route("/vendors/<int:vendor_id>", methods=['DELETE'])
def delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    return jsonify({})

#####################################################################
#                                                                   #
#####################################################################
@vendor_page.route("/_getjs_vendors/")
def getjs_vendors():
    vendors = Vendor.query.options(load_only("name")).all()
    js_vendors = []
    data = {}
    data['id'] = " "
    data['name'] = " "
    js_vendors.append(data)

    for vendor in vendors :

        data = {}
        data['id'] = str(vendor.id)
        data['name'] = vendor.name
        print('vendor.name : ' + vendor.name)
        js_vendors.append(data)

    return jsonify({'vendors': js_vendors})
