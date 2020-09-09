from lecopain.app import app
from lecopain.services.order_manager import OrderManager
from lecopain.services.report_manager import ReportManager
from lecopain.services.user_manager import UserManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify, send_file, send_from_directory
from flask_login import current_user
from lecopain.helpers.roles_utils import customer_login_required

app = Flask(__name__, instance_relative_config=True)

customer_report_page = Blueprint('customer_report_page', __name__,
                       template_folder='../templates')

orderServices= OrderManager()
reportServices = ReportManager()
userServices = UserManager()


#####################################################################
#                                                                   #
#####################################################################
@customer_report_page.route("/customer/reports", methods=['GET', 'POST'])
@customer_login_required
def reports():
    return render_template('/customer/reports/reports.html', title="Rapports")

#####################################################################
#                                                                   #
#####################################################################
@customer_report_page.route("/customer/reports/shipements", methods=['GET', 'POST'])
@customer_login_required
def reports_shipements():
    return render_template('/customer/reports/reports_shipments.html', title="Rapports")

@customer_report_page.route("/api/customer/reports/shipments/period/<string:period>/date/<string:day>", methods=['GET', 'POST'])
@customer_login_required
def list_shipements_customer_period(period, day):
    user_id = current_user.get_id()
    user = userServices.get_by_username(user_id)
    return jsonify({'reports': reportServices.get_reports_by_customer(user.account_id, period, day)})

