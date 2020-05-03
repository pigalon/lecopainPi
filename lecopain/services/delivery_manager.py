from lecopain import app, db
from lecopain.dao.models import Customer, CustomerOrder, Line

class DeliveryManager():

    def get_maps_from_deliveries(self, deliveries) :

        print(" deliveries 3-pret")
        customerMap = {}
        addressMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}
        print(" deliveries 3")
        for delivery in deliveries :
            print(" deliveries 3 - after" + str(delivery.customer_order_id))
            customerOrder = CustomerOrder.query.get_or_404(delivery.customer_order_id)
            print(" deliveries 4" + str(customerOrder))
            customer = Customer.query.get_or_404(customerOrder.customer_id)
            print(" deliveries 5" + str(customer))
            customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
            addressMap[customer.id] = customer.address #+ str( " " + customer.cp + " " + customer.city.encode("iso-8859-1" ) )


        for item in customerMap.items() :
            print (str(item))

        map['CUSTOMER'] = customerMap
        map['ADDRESS'] = addressMap
        
        
        return map