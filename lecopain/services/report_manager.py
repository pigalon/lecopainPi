
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.order_manager import OrderManager
from lecopain.services.shipment_manager import ShipmentManager
from datetime import datetime, date, timedelta
import xlsxwriter

class ReportManager():

    orderServices = OrderManager()
    shipmentServices = ShipmentManager()

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

    def get_reports_by_seller(self, seller_id, customer_id, period, day):
        days=[]
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)

        while start < end:
            end_day = start + timedelta(days=1)
            
            day = {}
            orders = self.orderServices.get_all_by_seller_customer_period_valid(
                seller_id, customer_id, start, end_day - timedelta(seconds=1))
            
            start = start + timedelta(seconds=1)
            day['date'] = start

            day = self.prepareDay(day, orders, start)
            days.append(day)
            start = end_day
        return days

    def get_main_amounts_by_seller(self, seller_id, customer_id, period, day):
        days = []
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)

        orders = self.orderServices.get_all_by_seller_customer_period_valid(
                seller_id, customer_id, start, end)

        return self.prepareAmount(orders)
    
    def get_reports_by_customer(self, customer_id, period, day):
        
        report = {}
        nb_products = 0
        shipping_price = 0.0
        shipments = self.shipmentServices.get_some_valid( customer_id, day, period)
        
        for shipment in shipments:
            nb_products = nb_products + shipment['nb_products']
            shipping_price = shipping_price + shipment['shipping_price']
        
        report['nb_shipments'] = len(shipments)
        report['nb_products'] = nb_products
        report['shipping_price'] = format(shipping_price, '.2f') 
        report['shipments'] = shipments                       

        return report
    
    def test_excel_report(self, seller_id, customer_id, period, day):

        days = self.get_reports_by_seller(seller_id, customer_id, period, day)
        workbook = xlsxwriter.Workbook('lecopain/hello.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        #cpt_days = 0
        for day in days :
            #cpt_days = cpt_days + 1
            for line in day['lines']:
                worksheet.write(row, col, line['customer'])
                #each="{product in line['products']}">
                #{product['name']}: x{product['quantity']},
                worksheet.write(row, col+1, str(line['products']))
                row = row + 1
            col = col + 2

        workbook.close()
        return 'hello.xlsx'
