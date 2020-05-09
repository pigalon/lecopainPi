from lecopain.dao.models import Customer, Order


class ShippingManager():

    def get_maps_from_shippings(self, shippings):

        customerMap = {}
        addressMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}
        for shipping in shippings:
            order = Order.query.get_or_404(
                shipping.order_id)
            customer = Customer.query.get_or_404(order.customer_id)
            customerMap[customer.id] = str(
                customer.firstname + " " + customer.lastname)
            # + str( " " + customer.cp + " " + customer.city.encode("iso-8859-1" ) )
            addressMap[customer.id] = customer.address

        map['CUSTOMER'] = customerMap
        map['ADDRESS'] = addressMap

        return map
