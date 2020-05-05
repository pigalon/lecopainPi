from lecopain.app import db
from datetime import datetime
from flask_login import UserMixin
from lecopain.app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from aenum import Enum


class OrderStatus_Enum(Enum):
    ANNULEE = "ANNULEE"
    DEFAUT = "DEFAUT"
    CREE = "CREE"
    TERMINEE = "TERMINEE"


class ShippingStatus_Enum(Enum):
    ANNULEE = "ANNULEE"
    LIVREE = "LIVREE"
    DEFAUT = "DEFAUT"
    CREE = "CREE"


class PaymentStatus_Enum(Enum):
    NON_PAYEE = "NON_PAYEE"
    PAYEE = "PAYEE"


class SubscriptionStatus_Enum(Enum):
    EN_COURS = "EN COURS"
    TERMINE = "TERMINE"


class SubscriptionFrequency_Enum(Enum):
    JOUR = "JOUR"
    SEMAINE = "SEMAINE"
    MOIS = "MOIS"


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    cp = db.Column(db.String(20))
    city = db.Column(db.String(50))
    email = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    orders = db.relationship('CustomerOrder', backref='owner', lazy=True)

    def __repr__(self):
        return "Customer('{self.firstname}','{self.lastname}','{self.email}')"

    def to_dict(self):
        orders_dict = []
        for order in self.orders:
            orders_dict.append(order.to_dict())
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'address': self.address,
            'cp': self.cp,
            'city': self.city,
            'email': self.email,
            'orders': orders_dict
        }


class CustomerOrder(db.Model):
    __tablename__ = 'customer_orders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)


<< << << < HEAD
vendorOrders = db.relationship(
    'VendorOrder', backref='customerOrder', lazy=True)
shipping = db.relationship('Shipping', uselist=False)
shipping_dt = db.Column(db.DateTime)
payement_status = db.Column(db.String(20), nullable=False)
subscription_id = db.Column(db.Integer, nullable=True)
== == == =
sellerOrders = db.relationship(
    'SellerOrder', backref='customerOrder', lazy=True)
shipping = db.relationship('Shipping', uselist=False)
shipping_dt = db.Column(db.DateTime)
payment_status = db.Column(db.String(20), nullable=False)
>>>>>> > master


def to_dict(self):
    return {
        'id': self.id,
        'title': self.title,
        'shipping_dt': self.shipping_dt,
        'status': self.status
    }


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
    selections = db.relationship(
        'CustomerOrder', secondary='lines', backref=db.backref('selected_products'))
    #selections_for_seller    = db.relationship('SellerOrder', secondary = 'seller_product', backref = db.backref('selected_products'))
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'sellers.id'), nullable=False)

    def __repr__(self):
        return "Product('{self.name}',{self.price}, '{self.description}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'status': self.status,
            'seller_id': self.seller_id
        }


class ProductStatus(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return "ProductStatus('{self.name}')"


class Line(db.Model):
    __tablename__ = 'lines'

    order_id = db.Column(db.Integer, db.ForeignKey(
        'customer_orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __repr__(self):
        return "CustomerOrder('{self.title}', '{self.status}', {customer_id} '{self.shipping_dt}')"

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }


class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    products = db.relationship('Product', backref='seller', lazy=True)
    sellerOrders = db.relationship('SellerOrder', backref='seller', lazy=True)

    def __repr__(self):
        return "Seller('{self.name}')"


class SellerOrder(db.Model):
    __tablename__ = 'seller_orders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'sellers.id'), nullable=False)
    customer_order_id = db.Column(db.Integer, db.ForeignKey(
        'customer_orders.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "SellerOrder('{self.title}', '{self.status}', {customer_order_id} '{self.seller_id}')"


class Shipping(db.Model):
    __tablename__ = 'shippings'
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), nullable=False)
    shipping_dt = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False)
    customer_order_id = db.Column(db.Integer, db.ForeignKey(
        'customer_orders.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)

    def __repr__(self):
        return "Seller('{self.reference}', '{self.shipping_dt}', '{self.status}', '{self.customer_order_id}')"


class ShippingStatus(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return "ShippingStatus('{self.name}')"


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    joined_at = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.password}')"

    def get_id(self):
        return self.username

    def is_active(self):
        return True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return " "


@login_manager.user_loader
def get_user(username):
    return User.query.filter(User.username == username).first()


class Subscription(db.Model):

    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    frequency = db.Column(db.String(1))
    days_in = db.Column(db.String(20))
    days_out = db.Column(db.String(20))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    status = db.Column(db.String(40))
    payement_status = db.Column(db.String(20), nullable=False)
    promotion = db.Column(db.String(200))


class Subscription_product(db.Model):
    __tablename__ = 'subscription_product'

    subscription_id = db.Column(db.Integer, db.ForeignKey(
        'subscriptions.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'subscription_id': self.subscription_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }


class Subscription(db.Model):

    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    frequency = db.Column(db.String(1))
    number_day = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    status = db.Column(db.String(40))
    payement_status = db.Column(db.String(20), nullable=False)
    promotion = db.Column(db.String(200))


class Subscription_product(db.Model):
    __tablename__ = 'subscription_product'

    subscription_id = db.Column(db.Integer, db.ForeignKey(
        'subscriptions.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'subscription_id': self.subscription_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }
