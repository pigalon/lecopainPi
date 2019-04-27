from lecopain import app, db
from lecopain.models import Customer, Order, Order_product

class DeliveryManager():

    def get_maps_from_deliveries(self, deliveries) :

        customerMap = {}
        addressMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}

        for delivery in deliveries :
            customer = Customer.query.get_or_404(delivery.customer_id)
            customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
            addressMap[customer.id] = customer.address #+ str( " " + customer.cp + " " + customer.city.encode("iso-8859-1" ) )


        for item in customerMap.items() :
            print (str(item))

        map['CUSTOMER'] = customerMap
        map['ADDRESS'] = addressMap
        
        return map