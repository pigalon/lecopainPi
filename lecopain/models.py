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
    #products = db.relationship("Product", secondary="orders")

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
    selections = db.relationship('Order', secondary = 'order_product', backref=db.backref('selected_products'))
    #customers = db.relationship("Customer", secondary="orders")
    #orders = db.relationship('Order', secondary = 'order_product')
   

    def __repr__(self):
        return "Product('{self.name}',{self.price}, '{self.description}')"

class Order_product(db.Model):
    __tablename__ = 'order_product'
   
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    order_dt = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    #product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
       
    #customer = db.relationship(Customer, backref=db.backref("orders", cascade="all, delete-orphan"))
    #product = db.relationship(Product, backref=db.backref("orders", cascade="all, delete-orphan"))
    

    #products = db.relationship('Product', secondary = 'order_product')

    def __repr__(self):
        return "Order('{self.title}', {customer_id} '{self.order_dt}')"
