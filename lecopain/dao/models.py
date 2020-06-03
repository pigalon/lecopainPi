from lecopain.app import db, ma
from datetime import datetime
from flask_login import UserMixin
from lecopain.app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from aenum import Enum
from marshmallow import fields
from marshmallow_sqlalchemy import (ModelSchema, SQLAlchemySchema, SQLAlchemyAutoSchema, auto_field)



class OrderStatus_Enum(Enum):
    ANNULEE = "ANNULEE"
    DEFAUT = "DEFAUT"
    CREE = "CREE"
    TERMINEE = "TERMINEE"


class ShippingStatus_Enum(Enum):
    NON = "NON"
    OUI = "OUI"


class PaymentStatus_Enum(Enum):
    NON = "NON"
    OUI = "OUI"


class SubscriptionStatus_Enum(Enum):
    CREE = "CREE"
    TERMINE = "TERMINE"


class SubscriptionFrequency_Enum(Enum):
    JOUR = "JOUR"
    SEMAINE = "SEMAINE"
    MOIS = "MOIS"
    

class Category_Enum(Enum):
    ARTICLE = "ARTICLE"
    COURSETTE = "COURSETTE"
    DRIVE = "DRIVE"



class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    cp = db.Column(db.String(20))
    city = db.Column(db.String(50))
    nb_orders = db.Column(db.Integer, default=0)
    nb_subscriptions = db.Column(db.Integer, default=0)
    email = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    orders = db.relationship('Order', backref='owner', lazy=True)
    subscriptions = db.relationship('Subscription', backref='owner', lazy=True)

    def __repr__(self):
        return "Customer('{self.firstname}','{self.lastname}','{self.email}')"

    # def to_dict(self):
    #     orders_dict = []
    #     for order in self.orders:
    #         orders_dict.append(order.to_dict())
    #     return {
    #         'id': self.id,
    #         'firstname': self.firstname,
    #         'lastname': self.lastname,
    #         'address': self.address,
    #         'cp': self.cp,
    #         'city': self.city,
    #         'email': self.email,
    #         'orders': orders_dict
    #     }

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    customer = db.relationship('Customer')
    status = db.Column(db.String(20), nullable=False,
                       default=OrderStatus_Enum.CREE.value)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'sellers.id'), nullable=False)
    seller = db.relationship('Seller')
    price = db.Column(db.Float)
    nb_products = db.Column(db.Integer)
    shipping_price = db.Column(db.Float)
    shipping_status = db.Column(
        db.String(20), nullable=False, default=ShippingStatus_Enum.NON.value)
    shipping_dt = db.Column(db.DateTime)
    shipping_address = db.Column(db.String(200))
    shipping_cp = db.Column(db.String(20))
    shipping_city = db.Column(db.String(50))

    payment_status = db.Column(
        db.String(20), nullable=False, default=PaymentStatus_Enum.NON.value)
    shipping_rules = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(20), nullable=True, default=Category_Enum.ARTICLE.value)
    products = db.relationship(
        "Product", secondary='lines', viewonly=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey(
        'subscriptions.id'), nullable=True)
    subscription = db.relationship('Subscription', backref=db.backref(
        "subscriptions", cascade="all, delete-orphan"))

    def add_line(self, line):
        self.lines.append(line)

    def __repr__(self):
        return '<Order {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'shipping_dt': self.shipping_dt,
            'status': self.status,
            'customer_id': self.customer_id
        }

class OrderStatus(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return "OrderStatus('{self.name}')"

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default='DISPONIBLE')
    orders = db.relationship("Order", secondary='lines', viewonly=True)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'sellers.id'), nullable=False)
    seller = db.relationship('Seller')
    category = db.Column(db.String(20), default=Category_Enum.ARTICLE.value)

    def __repr__(self):
        return "Product('{self.name}',{self.price})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'seller_id': self.seller_id,
            'category':self.category
        }


class ProductStatus(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return "ProductStatus('{self.name}')"


class Line(db.Model):
    __tablename__ = 'lines'
    __table_args__ = {'extend_existing': True}

    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    order = db.relationship(Order, backref=db.backref(
        "lines", cascade="all, delete-orphan"))
    product = db.relationship(Product, backref=db.backref(
        "lines", cascade="all, delete-orphan"))

    def __repr__(self):
        return '<Line {}>'.format(str(self.order.id)+" "+self.product.name)

    def __init__(self, order=None, product_id=None, quantity=None, price=None):
        self.order = order
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }


class Seller(db.Model):
    __tablename__ = 'sellers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    nb_orders = db.Column(db.Integer, default=0)
    nb_subscriptions = db.Column(db.Integer, default=0)
    products = db.relationship('Product', backref='owner', lazy=True)
    orders = db.relationship('Order', backref='recipient', lazy=True)

    def __repr__(self):
        return "Seller('{self.name}')"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
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
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    customer = db.relationship('Customer')
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'sellers.id'), nullable=False)
    seller = db.relationship('Seller')
    start_dt = db.Column(db.Date)
    end_dt = db.Column(db.Date)
    status = db.Column(db.String(40), default=SubscriptionStatus_Enum.CREE.value)
    payment_status = db.Column(db.String(20), nullable=False)
    promotion = db.Column(db.String(200))
    price = db.Column(db.Float, default=0.0)
    shipping_price = db.Column(db.Float, default=0.0)
    nb_products = db.Column(db.Integer, default=0)
    nb_orders = db.Column(db.Integer, default=0)
    category = db.Column(
        db.String(20), default=Category_Enum.ARTICLE.value)

    days = db.relationship('SubscriptionDay', backref='week',
                           lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='subref', lazy=True)



class SubscriptionDay(db.Model):
    __tablename__ = 'subscription_days'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey(
        'subscriptions.id'))
    subscription = db.relationship('Subscription')
    day_of_week = db.Column(db.Integer)
    nb_products = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    shipping_price = db.Column(db.Float, default=0.0)
    products = db.relationship(
        "Product", secondary='subscription_lines', viewonly=True)

    def add_products(self, items):
        for product_id, qty, price in items:
            self.lines.append(Line(
                order=self, product_id=product_id, quantity=qty, price=price))

    def add_line(self, line):
        self.lines.append(line)

    def to_dict(self):
        return {
            'subscription_id': self.subscription_id,
            'day_of_week': self.day_of_week
        }


class SubscriptionLine(db.Model):
    __tablename__ = 'subscription_lines'
    __table_args__ = {'extend_existing': True}

    subscription_day_id = db.Column(db.Integer, db.ForeignKey(
        'subscription_days.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    subscription_day = db.relationship(SubscriptionDay, backref=db.backref(
        "lines", cascade="all, delete-orphan"))
    product = db.relationship(Product, backref=db.backref(
        "subscription_lines"))
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'subscription_day_id': self.subscription_day_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }



class CustomerSchema(SQLAlchemyAutoSchema):

    class Meta:
        # Fields to expose
        model = Customer
        load_instance = True

class SellerSchema(SQLAlchemyAutoSchema):

    class Meta:
        # Fields to expose
        model = Seller
        load_instance = True


class ProductSchema(SQLAlchemyAutoSchema):

    class Meta:
        # Fields to expose
        model = Product
        load_instance = True

class LineSchema(SQLAlchemyAutoSchema):
    product_name = fields.Method("format_product_name", dump_only=True)
    price = fields.Method("format_price", dump_only=True)
    product_id = fields.Method("format_product_id", dump_only=True)

    class Meta:
        # Fields to expose
        model = Line
        load_instance = True

    def format_price(self, line):
        return "{}".format(line.price)

    def format_product_name(self, line):
        return "{}".format(line.product.name)
    
    def format_product_id(self, line):
        return "{}".format(line.product.id)



class OptimizedCustomerSchema(SQLAlchemySchema):

    class Meta:
        # Fields to expose
        model = Customer
        load_instance = True
    id = auto_field()
    firstname = auto_field()
    lastname = auto_field()

class OrderSchema(SQLAlchemyAutoSchema):
    customer_name = fields.Method("format_customer_name", dump_only=True)
    seller_name = fields.Method("format_seller_name", dump_only=True)
    subscription_id = fields.Method(
        "format_subscription_id", dump_only=True)

    class Meta:
        # Fields to expose
        model = Order
        load_instance = True
        include_relationships = True

    def format_customer_name(self, order):
        return "{}, {}".format(order.customer.firstname, order.customer.lastname)

    def format_seller_name(self, order):
        return "{}".format(order.seller.name)

    def format_subscription_id(self, order):
        if order.subscription != None:
            return "{}".format(order.subscription.id)

class CompleteOrderSchema(SQLAlchemyAutoSchema):
    customer_name = fields.Method("format_customer_name", dump_only=True)
    customer_id = fields.Method("format_customer_id", dump_only=True)
    seller_name = fields.Method("format_seller_name", dump_only=True)
    seller_id = fields.Method("format_seller_id", dump_only=True)
    nb_products = fields.Method("format_nb_products", dump_only=True)
    lines = fields.Method("format_lines", dump_only=True)
    shipping_formatted_dt = fields.Method("format_shipping_dt", dump_only=True)

    class Meta:
        # Fields to expose
        model = Order
        load_instance = True
        include_relationships = True

    def format_customer_name(self, order):
        return "{}, {}".format(order.customer.firstname, order.customer.lastname)

    def format_customer_id(self, order):
        return "{}".format(order.customer.id)

    def format_seller_name(self, order):
        return "{}".format(order.seller.name)

    def format_seller_id(self, order):
        return "{}".format(order.seller.id)

    def format_nb_products(self, order):
        nb_products = 0
        for line in order.lines:
            nb_products = nb_products + line.quantity
        return nb_products

    def format_lines(self, order):
        lines = []
        line_schema = LineSchema(many=False)
        for line in order.lines:
            lines.append(line_schema.dump(line))
        return lines

    def format_shipping_dt(self, order):
        return order.shipping_dt.strftime('%A %d %B %Y')

class OptimizedProductSchema(SQLAlchemySchema):

    class Meta:
        # Fields to expose
        model = Product
        load_instance = True
    id = auto_field()
    name = auto_field()
    seller_id = auto_field()

class ProductSchema(SQLAlchemyAutoSchema):

    class Meta:
        # Fields to expose
        model = Product
        load_instance = True
        include_relationships = True

class SubscriptionSchema(SQLAlchemyAutoSchema):
    customer_name = fields.Method("format_customer_name", dump_only=True)
    seller_name = fields.Method("format_seller_name", dump_only=True)
    start_formatted_dt = fields.Method("format_start_dt", dump_only=True)
    end_formatted_dt = fields.Method("format_end_dt", dump_only=True)

    class Meta:
        # Fields to expose
        model = Subscription
        load_instance = True
        include_relationships = True

    def format_customer_name(self, subscription):
        return "{}, {}".format(subscription.customer.firstname, subscription.customer.lastname)

    def format_seller_name(self, subscription):
        return "{}".format(subscription.seller.name)

    def format_start_dt(self, subscription):
        return subscription.start_dt.strftime('%A %d %B %Y')

    def format_end_dt(self, subscription):
        return subscription.end_dt.strftime('%A %d %B %Y')
    

class CompleteSubscriptionSchema(SQLAlchemyAutoSchema):
    customer_name = fields.Method("format_customer_name", dump_only=True)
    seller_name = fields.Method("format_seller_name", dump_only=True)
    seller_id = fields.Method("format_seller_id", dump_only=True)
    start_formatted_dt = fields.Method("format_start_dt", dump_only=True)
    end_formatted_dt = fields.Method("format_end_dt", dump_only=True)
    days = fields.Method("format_days", dump_only=True)
    

    class Meta:
        # Fields to expose
        model = Subscription
        load_instance = True
        include_relationships = True

    def format_customer_name(self, subscription):
        return "{}, {}".format(subscription.customer.firstname, subscription.customer.lastname)

    def format_seller_name(self, subscription):
        return "{}".format(subscription.seller.name)
    
    def format_seller_id(self, subscription):
        return "{}".format(subscription.seller.id)

    def format_start_dt(self, subscription):
        return subscription.start_dt.strftime('%A %d %B %Y')

    def format_end_dt(self, subscription):
        return subscription.end_dt.strftime('%A %d %B %Y')
    
    def format_days(self, subscription):
        days = []
        day_schema = SubscriptionDaySchema(many=False)
        for day in subscription.days:
            days.append(day_schema.dump(day))
        return days

class SubscriptionLineSchema(SQLAlchemyAutoSchema):
    product_name = fields.Method("format_product_name", dump_only=True)
    product_id = fields.Method("format_product_id", dump_only=True)
    product_category = fields.Method("format_product_category", dump_only=True)

    class Meta:
        # Fields to expose
        model = SubscriptionLine
        load_instance = True

    def format_product_name(self, subscription_line):
        return "{}".format(subscription_line.product.name)

    def format_product_id(self, subscription_line):
        return "{}".format(subscription_line.product.id)


    def format_product_category(self, subscription_line):
        return "{}".format(subscription_line.product.category)



class SubscriptionDaySchema(SQLAlchemyAutoSchema):

    class Meta:
        # Fields to expose
        model = SubscriptionDay
        load_instance = True
        include_relationships = True
        

class CompleteSubscriptionDaySchema(SQLAlchemyAutoSchema):
    
    customer_name = fields.Method("format_customer_name", dump_only=True)
    customer_city = fields.Method("format_customer_city", dump_only=True)
    seller_name = fields.Method("format_seller_name", dump_only=True)
    seller_id = fields.Method("format_seller_id", dump_only=True)
    lines = fields.Method("format_lines", dump_only=True)
    class Meta:
        # Fields to expose
        model = SubscriptionDay
        load_instance = True
        include_relationships = True

    def format_customer_name(self, subscription_day):
        return "{}, {}".format(subscription_day.subscription.customer.firstname, subscription_day.subscription.customer.lastname)

    def format_seller_name(self, subscription_day):
        return "{}".format(subscription_day.subscription.seller.name)
    
    def format_seller_id(self, subscription_day):
        return "{}".format(subscription_day.subscription.seller.id)

    def format_lines(self, subscription_day):
        lines = []
        line_schema = SubscriptionLineSchema(many=False)
        for line in subscription_day.lines:
            lines.append(line_schema.dump(line))
        return lines
    
    def format_customer_city(self, subscription_day):
        return "{}".format(subscription_day.subscription.customer.city)


