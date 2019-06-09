from datetime import datetime

from lecopain import app, db
from lecopain.dao.customer import Customer, CustomerOrder
from lecopain.dto.BoughtProduct import BoughtProduct
from lecopain.dao.models import (Delivery, Order_product, Product, Vendor,
                             VendorOrder)


class OrderManager()                       : 

    def get_resume_products_list_from_orders(self, orders):
        products = []
        for order in orders :
            for product in order.selected_products :
                
                
                order_product = Order_product.query.filter(Order_product.order_id == order.id).filter(Order_product.product_id == product.id).first()
                
                lenght_list = len(products)
                bAdded = False
                
                for index, item in enumerate(products):
                    if item.product.id == product.id:
                        products[index].quantity += order_product.quantity
                        bAdded = True
                    
                if(len(products)<1 or bAdded == False):
                    products.append(BoughtProduct(product=product, quantity=order_product.quantity))
        return products

    ##############################################
    # MAPS from ORDERS => total and quantity and customer
    ###############################################
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
            quantity = 0
            for bought_item in bought_items:
                total += bought_item.price  * bought_item.quantity
                quantity += bought_item.quantity
                

            totalMap[order.id]       = total
            nb_productsMap[order.id] = quantity  


        map['CUSTOMER']                    = customerMap
        map['NB_PRODUCTS']                 = nb_productsMap
        map['TOTAL']                       = totalMap
        
        return map
    
    #########################################@
    #
    def create_customer_order(self, order, tmp_products, tmp_quantities, tmp_prices): 
        products = {}
        order.created_at = datetime.now()

        order = self.create_product_purchases(order, tmp_products, tmp_quantities, tmp_prices)
            
        self.create_default_delivery(order)

        
    #########################################@
    #
    def update_customer_order(self, order, products, quantities, prices): 
        
        order.created_at = datetime.now()
        
        self.delete_every_order_dependencies(order)
        
        order = self.create_product_purchases(order, products, quantities, prices)
        
        delivery = Delivery.query.filter(Delivery.customer_order_id == order.id).first()
        db.session.commit()
        

    #########################################@
    #
    def create_product_purchases(self, order, tmp_products, tmp_quantities, tmp_prices):
        order = self.create_products_for_specific_order(order=order, tmp_products=tmp_products)
        db.session.add(order)
        db.session.commit()

        self.create_corresponding_purchases(order=order, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)

        vendorOrders = self.generate_vendor_orders(order=order)
        for vendorOrder in vendorOrders :
           db.session.add(vendorOrder)
        return order
    #########################################@
    #
    def create_products_for_specific_order(self, order, tmp_products):
        
        for i in range(0,len(tmp_products)): 
            product = Product.query.get(tmp_products[i])
            order.selected_products.append(product)
     
        return order
    
    ##########################################
    #
        def create_default_delivery(self, order):
            delivery = Delivery(reference=order.title ,delivery_dt=order.delivery_dt, status='NON_LIVREE', customer_order_id=order.id, customer_id=order.customer_id)     
            db.session.add(delivery)
            db.session.commit()
    
    
    #########################################
    #
    def delete_every_order_dependencies(self, order):
        # delete order_product relation to recreate
        Order_product.query.filter(Order_product.order_id == order.id).delete()
        
        # TODO : missing delete vendor order !!!!
        VendorOrder.query.filter(VendorOrder.customer_order_id == order.id).delete()
        
        
    #########################################@
    #
    def create_order_with_his_products(self, order, tmp_products):
        
        for i in range(0,len(tmp_products)): 
            product = Product.query.get(tmp_products[i])
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
