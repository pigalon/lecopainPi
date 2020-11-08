
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.order_manager import OrderManager
from lecopain.services.shipment_manager import ShipmentManager
from datetime import datetime, date, timedelta
import xlsxwriter
import json

class ReportManager():

    orderServices = OrderManager()
    shipmentServices = ShipmentManager()

    def prepareAmount(self, orders, dt=None):
        amount = {'price': 0.0,
                    'nb_products': 0, 'nb_orders': 0}
        products = []
        amount_shipping_price = 0.0
        amount_price = 0.0
        for order in orders:
            shipping_day = order['shipping_dt'].day
            if dt is None or int(shipping_day) == dt.day:

                amount_price = (amount_price + order['price'])
                amount['nb_products'] = int(amount['nb_products']) + \
                order['nb_products']
        
        amount['price'] = format(amount_price, '.2f')
        amount['products'] = self.orderServices.extract_products_from_orders(orders, dt)
        amount['nb_orders'] = len(orders)
        return amount


    def prepareLines_by_customer(self, orders, dt):
        lines = []

        for order in orders:
            shipping_day = order['shipping_dt'].day
            if int(shipping_day) == dt.day:
                line = {'customer':order['customer_name'], 'address':order['customer_address']}
                line['products'] = []
                for order_line in order['lines']:
                    line['products'].append({'name':order_line['product_short_name'], 'quantity':order_line['quantity']})
                lines.append(line)
        return lines

    def prepareDay(self, day, orders, dt):
        day['amount'] = self.prepareAmount(orders, dt)
        day['lines'] = self.prepareLines_by_customer(orders, dt)
        return day

    def get_reports_by_seller(self, seller_id, customer_id, period, day):
        days=[]
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)
        
        if period == Period_Enum.DAY.value:
            start = start + timedelta(seconds=1)
        
        while start <= end:
            end_day = start + timedelta(days=1)
            
            day = {}
            orders = self.orderServices.get_all_by_seller_customer_period_valid(
                seller_id, customer_id, start, end_day)
            
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
        workbook = xlsxwriter.Workbook('/tmp/report.xlsx')
        worksheet = workbook.add_worksheet()
        

        row = 0
        col = 0
        column_width = 0
       
        cell_format_date = workbook.add_format({'num_format': 'ddd dd mmm yyyy'})
        cell_format_date.set_pattern(1)  # This is optional when using a solid fill.
        cell_format_date.set_bg_color('yellow')
        cell_format_date.set_border()
        cell_format_date.set_align('center')
        
        cell_format_amounts = workbook.add_format()
        cell_format_amounts.set_pattern(1)  # This is optional when using a solid fill.
        cell_format_amounts.set_bg_color('#e6e8e8')
        cell_format_amounts.set_border()
        cell_format_amounts.set_align('center')
        
        cell_format_name = workbook.add_format()
        cell_format_name.set_pattern(1)  # This is optional when using a solid fill.
        cell_format_name.set_bg_color('#bffcf9')
        cell_format_name.set_left()
        cell_format_name.set_right()
        cell_format_name.set_text_wrap()
        
        cell_format_products = workbook.add_format()
        cell_format_products.set_pattern(1)  # This is optional when using a solid fill.
        cell_format_products.set_bg_color('#ffffff')
        cell_format_products.set_left()
        cell_format_products.set_right()
        
        
        for day in days :
            row = 0
            worksheet.merge_range(row, col, row, col+1, '')
            worksheet.write_datetime(row, col, day['date'], cell_format_date)
            row = row + 1
            amounts_line = 'Prix : ' + str(day['amount']['price']) + ' € - Nb. commandes : ' + str(day['amount']['nb_orders']) + ' - Totaux :'
            for product_amounts in day['amount']['products']:
                    amounts_line = amounts_line + (str(product_amounts['short_name']) + ' x'+ str(product_amounts['quantity']) + ', ')
            worksheet.merge_range(row, col, row, col+1, '')
            worksheet.write(row, col, amounts_line, cell_format_amounts)
            row = row + 1
            for line in day['lines']:
                worksheet.set_row(row, 40)
                worksheet.set_column(col, col, 20)
                worksheet.write(row, col, line['customer'] +'\n'+ line['address'], cell_format_name)
                products_line = ''
                for line_product in line['products']:
                    products_line = products_line + (str(line_product['name']) + ' x'+ str(line_product['quantity']) + ', ')
                if (len(products_line) > column_width):
                    width = len(products_line)
                    worksheet.set_column(col+1, col+1, 30)
                worksheet.write(row, col+1, products_line, cell_format_products)
                row = row + 1
            col = col + 3
            column_width = 0

        workbook.close()
        return '/tmp/report.xlsx'
    
