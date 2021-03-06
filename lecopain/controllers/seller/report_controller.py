from lecopain.app import app
from lecopain.services.order_manager import OrderManager
from lecopain.services.user_manager import UserManager
from lecopain.services.report_manager import ReportManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify, send_file, send_from_directory
from flask_login import login_required, current_user

app = Flask(__name__, instance_relative_config=True)

seller_report_page = Blueprint('seller_report_page', __name__,
                    template_folder='../templates')

orderServices= OrderManager()
userServices= UserManager()
reportServices = ReportManager()


#####################################################################
#                                                                   #
#####################################################################
@seller_report_page.route("/seller/reports", methods=['GET', 'POST'])
@login_required
def reports():
    return render_template('/seller/reports/reports.html', title="Rapports")


#####################################################################
#                                                                   #
#####################################################################
@seller_report_page.route("/seller/api/reports/days/period/<string:period>/date/<string:day>/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def list_orders_seller_period(period, day, customer_id):
    user_id = current_user.get_id()
    user = userServices.get_by_username(user_id)
    seller_id=user.account_id
    return jsonify({'days': reportServices.get_reports_by_seller(seller_id, customer_id, period, day)})


@seller_report_page.route("/seller/api/reports/amounts/period/<string:period>/date/<string:day>/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def amounts_seller_period(period, day, customer_id):
    user_id = current_user.get_id()
    user = userServices.get_by_username(user_id)
    seller_id=user.account_id
    return jsonify({'amounts': reportServices.get_main_amounts_by_seller(seller_id, customer_id, period, day)})

@seller_report_page.route("/seller/api/reports/excel/period/<string:period>/date/<string:day>/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def excel(period, day, customer_id):
    user_id = current_user.get_id()
    user = userServices.get_by_username(user_id)
    seller_id=user.account_id
    return send_file(reportServices.test_excel_report(seller_id, customer_id, period, day), as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

