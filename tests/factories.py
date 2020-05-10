from factory.alchemy import SQLAlchemyModelFactory
from lecopain.dao.models import User, Product, Seller, Customer, Order
from werkzeug.security import generate_password_hash
from lecopain.app import db
import factory
import unicodedata
from factory.faker import faker
from datetime import datetime, timedelta


class UserFactory(SQLAlchemyModelFactory):

    fake = faker.Faker()

    class Meta:
        model = User

    username = factory.Faker('name')
    password = generate_password_hash("password")
    @factory.lazy_attribute
    def email(self):
        # Convert to plain ascii text
        clean_name = (unicodedata.normalize('NFKD', self.username)
                      .encode('ascii', 'ignore')
                      .decode('utf8'))
        return u'%s@example.com' % clean_name


class AdminFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    username = 'admin'
    password = generate_password_hash('password')
    email = "admin@test.com"


class SellerFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Seller
        sqlalchemy_session = db.session
    name = factory.Faker('company')
    email = 'seller@mail.com'


class ProductFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Product
        sqlalchemy_session = db.session
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    price = factory.Faker('pyfloat', right_digits=2,)

    seller = factory.SubFactory(SellerFactory)


class CustomerFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Customer
        sqlalchemy_session = db.session
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    address = factory.Faker('address')
    cp = factory.Faker('building_number')
    city = factory.Faker('city')
    email = factory.Faker('ascii_email')

    created_at = factory.Faker('date_time')


class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = db.session
    title = 'test'
    status = "ANNULEE"
    created_at = factory.Faker('date_time')
    payment_status = "TEST"
    shipping_dt = factory.Faker(
        'date_time_between', start_date='-6d', end_date='+6d', tzinfo=None)

    customer = factory.SubFactory(CustomerFactory)
    seller = factory.SubFactory(SellerFactory)
    
    
class SellerFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Seller
        sqlalchemy_session = db.session
    name = factory.Faker('company')
    email = factory.Faker('ascii_email')
        
