from lecopain.models import Vendor
from lecopain.services.vendor_manager import VendorManager
from lecopain import app, db
from lecopain.form import VendorForm
from flask import Blueprint, render_template, redirect, url_for, Flask


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
        return redirect(url_for('vendors'))
    return render_template('/vendors/create_vendor.html', title='Formulaire Vendeur', form=form)

@vendor_page.route("/vendors/<int:vendor_id>")
def vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    return render_template('/vendors/vendor.html', vendor=vendor)
