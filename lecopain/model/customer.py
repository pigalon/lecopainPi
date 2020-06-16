from lecopain.app import db, ma
from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import ( SQLAlchemySchema, SQLAlchemyAutoSchema, auto_field)

class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    cp = db.Column(db.String(20))
    city = db.Column(db.String(50))
    nb_shipments = db.Column(db.Integer, default=0)
    nb_subscriptions = db.Column(db.Integer, default=0)
    email = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    shipments = db.relationship('Shipment', backref='owner', lazy=True)
    subscriptions = db.relationship('Subscription', backref='owner', lazy=True)

    def __repr__(self):
        return "Customer('{self.firstname}','{self.lastname}','{self.email}')"

class CustomerSchema(SQLAlchemyAutoSchema):

    class Meta:
        # Fields to expose
        model = Customer
        load_instance = True
        
class OptimizedCustomerSchema(SQLAlchemySchema):

    class Meta:
        # Fields to expose
        model = Customer
        load_instance = True
    id = auto_field()
    firstname = auto_field()
    lastname = auto_field()


