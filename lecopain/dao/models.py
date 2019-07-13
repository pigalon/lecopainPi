from lecopain import db
from datetime import datetime
from flask_login import UserMixin
from lecopain import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model)        : 
    __tablename__               = 'customers'
    id                          = db.Column(db.Integer, primary_key                             = True)
    firstname                   = db.Column(db.String(50), nullable                             = False)
    lastname                    = db.Column(db.String(50), nullable                             = False)
    address                     = db.Column(db.String(200))
    cp                          = db.Column(db.String(20))
    city                        = db.Column(db.String(50))
    email                       = db.Column(db.String(200), nullable                            = False)
    created_at                  = db.Column(db.DateTime, nullable                               = False, default = datetime.utcnow)
    orders                      = db.relationship('CustomerOrder', backref                      = 'owner', lazy  = True)

    def __repr__(self)          : 
        return "Customer('{self.firstname}','{self.lastname}','{self.email}')"

    def to_dict(self)           : 
        orders_dict             = []
        for order in self.orders: 
            orders_dict.append(order.to_dict())
        return {
            'id'                : self.id,
            'firstname'         : self.firstname,
            'lastname'          : self.lastname,
            'address'           : self.address,
            'cp'                : self.cp,
            'city'              : self.city,
            'email'             : self.email,
            'orders'            : orders_dict
        }

class CustomerOrder(db.Model)   : 
    __tablename__               = 'customer_orders'
    id                          = db.Column(db.Integer, primary_key                             = True)
    title                       = db.Column(db.String(50), nullable                             = False)
    created_at                  = db.Column(db.DateTime, nullable                               = False, default = datetime.utcnow)
    customer_id                 = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable = False)
    status                      = db.Column(db.String(20), nullable                             = False)
    vendorOrders                = db.relationship('VendorOrder', backref = 'customerOrder', lazy = True)
    delivery                    = db.relationship('Delivery', uselist=False)
    delivery_dt                 = db.Column(db.DateTime)
    payement_status             = db.Column(db.String(20), nullable                             = False)
    
    
    def to_dict(self)           : 
        return {
            'id'                : self.id,
            'title'             : self.title,
            'delivery_dt'       : self.delivery_dt,
            'status'            : self.status
        }

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
    
    def to_dict(self)         : 
        return {
            'order_id'        : self.order_id,
            'product_id'      : self.product_id,
            'quantity'        : self.quantity,
            'price'           : self.price
        }


class Vendor(db.Model)        : 
    __tablename__             = 'vendors'
    id                        = db.Column(db.Integer, primary_key  = True)
    name                      = db.Column(db.String(50), nullable  = False)
    email                     = db.Column(db.String(200), nullable = False)
    products                  = db.relationship('Product', backref = 'vendor', lazy = True)
    vendorOrders              = db.relationship('VendorOrder', backref = 'vendor', lazy = True)
    

    def __repr__(self)        : 
        return "Vendor('{self.name}')"

class VendorOrder(db.Model)   : 
    __tablename__             = 'vendor_orders'
    id                        = db.Column(db.Integer, primary_key                                      = True)
    title                     = db.Column(db.String(50), nullable                                      = False)
    vendor_id                 = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable      = False)
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
    customer_id               = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable    = False)


    def __repr__(self)        : 
        return "Vendor('{self.reference}', '{self.delivery_dt}', '{self.status}', '{self.customer_order_id}')"

class DeliveryStatus(db.Model): 
    name                      = db.Column(db.String(50), primary_key                                   = True)

    def __repr__(self)        : 
        return "DeliveryStatus('{self.name}')"

class User(db.Model, UserMixin):
    __tablename__             = 'users'
    
    id                        = db.Column(db.Integer, primary_key = True)
    username                  = db.Column(db.String(50), nullable = False)
    email                     = db.Column(db.String(50), nullable = False)
    password                  = db.Column(db.String(100), nullable= False)
    joined_at                 = db.Column(db.DateTime)
    is_admin                  = db.Column(db.Boolean)


    def get_id(self):
        return self.username

    def is_active(self):
       return True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        print("psssss : " + str(self.password) + " - " + str(password))
        return check_password_hash(self.password, password)

    def __repr__(self):
       return " "

@login_manager.user_loader
def get_user(username):
  return User.query.filter(User.username == username).first()


#@login.request_loader
#def request_loader(request):
    
#    username = request.form.get('username')
#    user = User.query.filter(User.username == username).first()
    
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
#    user.is_authenticated = request.form['password'] == user.password

#    return user


