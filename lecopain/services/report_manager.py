
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.order_manager import OrderManager
from datetime import datetime, date, timedelta

class ReportManager():

    orderServices = OrderManager()

    def prepareAmount(self, orders):
        amount = {'shipping_price': 0.0, 'price': 0.0,
                  'nb_products': 0, 'nb_orders': 0}
        products = []
        for order in orders:
            amount['shipping_price'] = amount['shipping_price'] + float(order['shipping_price'])
            amount['price'] = float(amount['price']) + \
                order['price']
            amount['nb_products'] = int(amount['nb_products']) + \
                order['nb_products']
            # get numbers of each products for a list of orders !!!
            # amount by product type => get from lines quantity + id_product for key and product_short_name for display
            #for line in order.lines:
            #    line
            #    products[]
        self.orderServices.extract_products_from_orders(orders)
        amount['nb_orders'] = len(orders)
        return amount

    def prepareLines_by_customer(self, orders):
        lines = []
        return lines

    def prepareDay(self, day, orders):
        day['amount'] = self.prepareAmount(orders)
        day['lines'] = self.prepareLines_by_customer(orders)
        return day

    def get_reports_by_seller(self, seller_id, period, day):
        days=[]
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)
        while start <= end:
            day = {}
            day['date'] = start
            orders = self.orderServices.get_all_by_seller_period(
                seller_id, start, end)

            day = self.prepareDay(day, orders)
            days.append(day)
            start = start + timedelta(days=1)
        return days
