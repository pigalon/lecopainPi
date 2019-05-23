from lecopain import app, db
from lecopain.models import Order_product, Product, VendorOrder, Vendor, Delivery
from lecopain.dao.customer import Customer, CustomerOrder

class OrderManager()                       : 

    def get_maps_from_orders(self, orders) : 

        customerMap    = {}
        totalMap       = {}
        nb_productsMap = {}

        map            = {}

        for order in orders : 
            customer = Customer.query.get_or_404(order.customer_id)
            customerMap[order.id] = str(customer.firstname + " " + customer.lastname)
 
            bought_items = Order_product.query.filter(Order_product.order_id == order.id).all()
            total = 0
            for bought_item in bought_items:
                total = total + bought_item.price
                

            totalMap[order.id]       = total
            nb_productsMap[order.id] = len(bought_items)  

        for item in customerMap.items(): 
            print (str(item))

        map['CUSTOMER']                    = customerMap
        map['NB_PRODUCTS']                 = nb_productsMap
        map['TOTAL']                       = totalMap
        
        return map
    
    #########################################@
    #
    def create_customer_order(self, order, tmp_products, tmp_quantities, tmp_prices): 
        products = {}

        order = self.create_order_with_his_products(order=order, tmp_products=tmp_products)
        db.session.add(order)
        db.session.commit()           
        self.create_corresponding_purchases(order=order, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)
        #db.session.commit()
        
        vendorOrders = self.generate_vendor_orders(order=order)
        for vendorOrder in vendorOrders :
           db.session.add(vendorOrder)
        delivery = Delivery(reference=order.title ,delivery_dt=order.delivery_dt, status='NON_LIVREE', customer_order_id=order.id)     
        db.session.add(delivery)
        db.session.commit()
        

    #########################################@
    #
    def create_order_with_his_products(self, order, tmp_products):
        
        for i in range(0,len(tmp_products)): 
            product = Product.query.get(tmp_products[i])
            #print("product : " + product.id + " - " + product.name )
            order.selected_products.append(product)
     
        return order

    #########################################@
    #
    def create_corresponding_purchases(self, order, tmp_products, tmp_quantities, tmp_prices):
        
        for i in range(0,len(tmp_products)):
            bought_item = Order_product.query.filter(Order_product.order_id == order.id).filter(Order_product.product_id == tmp_products[i]).first()
            bought_item.quantity = tmp_quantities[i]
            bought_item.price = tmp_prices[i]

    #########################################@
    #
    def generate_vendor_orders(self, order):
        vendorOrders = []
        vendorIds = self.get_vendors_from_products(order)
        for vendorId in vendorIds:
            vendorOrders.append(VendorOrder(title=order.title, status='CREE', customer_order_id=order.id, vendor_id=vendorId))

        return vendorOrders
    
    #########################################@
    #
    def get_vendors_from_products(self, order): 
        vendorIds = set()
        for product in order.selected_products:
            vendorIds.add(product.vendor_id)
        return vendorIds
