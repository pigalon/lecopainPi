from factory.alchemy import SQLAlchemyModelFactory
from lecopain.dao.models import User, Product, Vendor
from werkzeug.security import generate_password_hash
import lecopain
import factory


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    username = str(factory.Faker('first_name'))
    password = generate_password_hash("password")
    email = username + "@test.com"


class AdminFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = lecopain.db.session

    username = 'admin'
    password = generate_password_hash('password')
    email = "admin@test.com"


class VendorFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Vendor
        sqlalchemy_session = lecopain.db.session
    name = 'Boulangerie Langlade'
    email = 'vendor@mail.com'


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = lecopain.db.session
    name = 'baguette'
    description = 'classique'
    price = 0.68

    vendor = factory.SubFactory(VendorFactory)
