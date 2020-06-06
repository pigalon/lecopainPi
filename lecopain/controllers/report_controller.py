from lecopain.app import app
from lecopain.services.order_manager import OrderManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

report_page = Blueprint('report_page', __name__,
                       template_folder='../templates')

orderServices= OrderManager()


#####################################################################
#                                                                   #
#####################################################################
@report_page.route("/reports", methods=['GET', 'POST'])
@login_required
def reports():
    return render_template('/reports/reports.html', title="Rapports")

#####################################################################
#                                                                   #
#####################################################################


@report_page.route("/api/reports/period/<string:period>/date/<string:day>/sellers/<int:seller_id>", methods=['GET', 'POST'])
@login_required
def list_orders_seller_period(period, day, seller_id):
    # select orders for specific seller
    #  - check the date
    #  - get the correct period day or week around the day
    
    #from each order create a line customer + products
    # group if both for 1 customer
    
    return jsonify({'orders': orderServices.get_all_by_seller_period(seller_id, period, day)})

#api/reports/period/day/date/06%2F06%2F2020/sellers/1