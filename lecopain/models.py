from lecopain import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    id =  db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    cp = db.Column(db.String(20))
    city = db.Column(db.String(50))
    email = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.relationship('Order', backref='owner', lazy=True)

    def __repr__(self):
        return "Customer('{self.firstname}','{self.lastname}','{self.email}')"

class OrderStatus(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return "OrderStatus('{self.name}')"

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float)
    status = db.Column(db.String(20))
    selections = db.relationship('Order', secondary = 'order_product', backref=db.backref('selected_products'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

    def __repr__(self):
        return "Product('{self.name}',{self.price}, '{self.description}')"

class ProductStatus(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return "ProductStatus('{self.name}')"

class Order_product(db.Model):
    __tablename__ = 'order_product'
   
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    order_dt = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    vendor_id = db.Column(db.Integer)
 
    def __repr__(self):
        return "Order('{self.title}', '{self.status}', {customer_id} '{self.order_dt}')"

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    products = db.relationship('Product', backref='vendor', lazy=True)

    def __repr__(self):
        return "Vendor('{self.name}')"
