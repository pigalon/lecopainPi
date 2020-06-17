
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.order_manager import OrderManager
from datetime import datetime, date, timedelta

class ReportManager():

    orderServices = OrderManager()

    def prepareAmount(self, orders):
        amount = {'price': 0.0,
                  'nb_products': 0, 'nb_orders': 0}
        products = []
        amount_shipping_price = 0.0
        amount_price = 0.0
        for order in orders:
            shipping_day = order['shipping_dt'].day

            #amount_shipping_price = amount_shipping_price + \
            #    float(order['shipping_price'])

            amount_price = (amount_price + order['price'])
            amount['nb_products'] = int(amount['nb_products']) + \
                order['nb_products']
        
        amount['price'] = format(amount_price, '.2f')
        amount['products'] = self.orderServices.extract_products_from_orders(orders)
        amount['nb_orders'] = len(orders)
        return amount

    def prepareLines_by_customer(self, orders, dt):
        lines = []

        for order in orders:
            shipping_day = order['shipping_dt'].day
            if int(shipping_day) == dt.day:
                line = {'customer':order['customer_name']}
                line['products'] = []
                for order_line in order['lines']:
                    line['products'].append({'name':order_line['product_short_name'], 'quantity':order_line['quantity']})
                lines.append(line)
        return lines

    def prepareDay(self, day, orders, dt):
        day['amount'] = self.prepareAmount(orders)
        day['lines'] = self.prepareLines_by_customer(orders, dt)
        return day

    def get_reports_by_seller(self, seller_id, period, day):
        days=[]
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)

        while start < end:
            end_day = start + timedelta(days=1)
            
            day = {}
            orders = self.orderServices.get_all_by_seller_period(
                seller_id, start, end_day - timedelta(seconds=1))
            
            start = start + timedelta(seconds=1)
            day['date'] = start

            day = self.prepareDay(day, orders, start)
            days.append(day)
            start = end_day
        return days

    def get_main_amounts_by_seller(self, seller_id, period, day):
        days = []
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)

        orders = self.orderServices.get_all_by_seller_period(
                seller_id, start, end)

        return self.prepareAmount(orders)

