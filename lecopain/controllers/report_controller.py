from lecopain.app import app
from lecopain.services.order_manager import OrderManager
from lecopain.services.report_manager import ReportManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

report_page = Blueprint('report_page', __name__,
                       template_folder='../templates')

orderServices= OrderManager()
reportServices = ReportManager()


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
@report_page.route("/reports/shipements", methods=['GET', 'POST'])
@login_required
def reports_shipements():
    return render_template('/reports/reports_shipments.html', title="Rapports")


#####################################################################
#                                                                   #
#####################################################################


@report_page.route("/api/reports/days/period/<string:period>/date/<string:day>/sellers/<int:seller_id>", methods=['GET', 'POST'])
@login_required
def list_orders_seller_period(period, day, seller_id):
   
    return jsonify({'days': reportServices.get_reports_by_seller(seller_id, period, day)})


@report_page.route("/api/reports/amounts/period/<string:period>/date/<string:day>/sellers/<int:seller_id>", methods=['GET', 'POST'])
@login_required
def amounts_seller_period(period, day, seller_id):

    return jsonify({'amounts': reportServices.get_main_amounts_by_seller(seller_id, period, day)})

@report_page.route("/api/reports/shipments/period/<string:period>/date/<string:day>/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def list_shipements_customer_period(period, day, customer_id):
   
    return jsonify({'reports': reportServices.get_reports_by_customer(customer_id, period, day)})

