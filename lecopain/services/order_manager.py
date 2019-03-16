from lecopain import app, db
from lecopain.models import Customer, Order, Order_product

class OrderManager():

    def get_maps_from_orders(self, orders) :

        customerMap = {}
        addressMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}

        for order in orders :
            customer = Customer.query.get_or_404(order.customer_id)
            customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
            addressMap[customer.id] = customer.address + str( " " + customer.cp + " " + customer.city.encode("iso-8859-1" ) )

            bought_items = Order_product.query.filter(Order_product.order_id == order.id).all()
            total = 0
            for bought_item in bought_items:
                total = total + bought_item.price
            totalMap[customer.id] = total
            nb_productsMap[customer.id] = len(bought_items)  

        for item in customerMap.items() :
            print (str(item))

        map['CUSTOMER'] = customerMap
        map['NB_PRODUCTS'] = nb_productsMap
        map['TOTAL'] = totalMap
        map['ADDRESS'] = addressMap
        
        return map