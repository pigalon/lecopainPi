from lecopain import db
from datetime import datetime
class OrderStatus(db.Model)   : 
    name                      = db.Column(db.String(50), primary_key                                   = True)

    def __repr__(self)        : 
        return "OrderStatus('{self.name}')"

class Product(db.Model)      : 
    __tablename__            = 'products'
    id                       = db.Column(db.Integer, primary_key = True)
    name                     = db.Column(db.String(50), nullable = False)
    description              = db.Column(db.String(250))
    price                    = db.Column(db.Float)
    status                   = db.Column(db.String(20))
    selections               = db.relationship('CustomerOrder', secondary = 'order_product', backref = db.backref('selected_products'))
    #selections_for_vendor    = db.relationship('VendorOrder', secondary = 'vendor_product', backref = db.backref('selected_products'))
    vendor_id                = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable = False)

    def __repr__(self)        : 
        return "Product('{self.name}',{self.price}, '{self.description}')"
    
    def to_dict(self)         : 
        return {
            'id'              : self.id,
            'name'            : self.name,
            'description'     : self.description,
            'price'           : self.price,
            'status'          : self.status,
            'vendor_id'       : self.vendor_id
        }

class ProductStatus(db.Model) : 
    name                      = db.Column(db.String(50), primary_key                                   = True)

    def __repr__(self)        : 
        return "ProductStatus('{self.name}')"

class Order_product(db.Model) : 
    __tablename__             = 'order_product'
   
    order_id                  = db.Column(db.Integer, db.ForeignKey('customer_orders.id'), primary_key = True)
    product_id                = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key        = True)
    quantity                  = db.Column(db.Integer)
    price                     = db.Column(db.Float)
 
    def __repr__(self)        : 
        return "CustomerOrder('{self.title}', '{self.status}', {customer_id} '{self.delivery_dt}')"

class Vendor(db.Model)        : 
    __tablename__             = 'vendors'
    id                        = db.Column(db.Integer, primary_key                                      = True)
    name                      = db.Column(db.String(50), nullable                                      = False)
    email                     = db.Column(db.String(200), nullable                                     = False)
    products                  = db.relationship('Product', backref                                     = 'vendor', lazy           = True)

    def __repr__(self)        : 
        return "Vendor('{self.name}')"

class VendorOrder(db.Model)   : 
    __tablename__             = 'vendor_orders'
    id                        = db.Column(db.Integer, primary_key                                      = True)
    title                     = db.Column(db.String(50), nullable                                      = False)
    vendor_id                 = db.Column(db.Integer, db.ForeignKey('vendor_orders.id'), nullable      = False)
    customer_order_id         = db.Column(db.Integer, db.ForeignKey('customer_orders.id'), nullable    = False)
    status                    = db.Column(db.String(20), nullable                                      = False)
    
    def __repr__(self)        : 
        return "VendorOrder('{self.title}', '{self.status}', {customer_order_id} '{self.vendor_id}')"

    

class Delivery(db.Model)      : 
    __tablename__             = 'deliveries'
    id                        = db.Column(db.Integer, primary_key                                      = True)
    reference                 = db.Column(db.String(50), nullable                                      = False)
    delivery_dt               = db.Column(db.DateTime)
    status                    = db.Column(db.String(20), nullable                                      = False)
    customer_order_id         = db.Column(db.Integer, db.ForeignKey('customer_orders.id'), nullable    = False)


    def __repr__(self)        : 
        return "Vendor('{self.reference}', '{self.delivery_dt}', '{self.status}', '{self.customer_order_id}')"

class DeliveryStatus(db.Model): 
    name                      = db.Column(db.String(50), primary_key                                   = True)

    def __repr__(self)        : 
        return "DeliveryStatus('{self.name}')"
