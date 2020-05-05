from lecopain.app import app, db
from lecopain.dao.models import Customer, CustomerOrder, Line


class ShippingManager():

    def get_maps_from_shippings(self, shippings):

        print(" shippings 3-pret")
        customerMap = {}
        addressMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}
        print(" shippings 3")
        for shipping in shippings:
            print(" shippings 3 - after" + str(shipping.customer_order_id))
            customerOrder = CustomerOrder.query.get_or_404(
                shipping.customer_order_id)
            print(" shippings 4" + str(customerOrder))
            customer = Customer.query.get_or_404(customerOrder.customer_id)
            print(" shippings 5" + str(customer))
            customerMap[customer.id] = str(
                customer.firstname + " " + customer.lastname)
            # + str( " " + customer.cp + " " + customer.city.encode("iso-8859-1" ) )
            addressMap[customer.id] = customer.address
        for item in customerMap.items():
            print(str(item))

        map['CUSTOMER'] = customerMap
        map['ADDRESS'] = addressMap

        return map
