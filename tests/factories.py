from factory.alchemy import SQLAlchemyModelFactory
from lecopain.dao.models import User, Product, Seller
from werkzeug.security import generate_password_hash
from lecopain.app import db
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
        sqlalchemy_session = db.session

    username = 'admin'
    password = generate_password_hash('password')
    email = "admin@test.com"


class SellerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Seller
        sqlalchemy_session = db.session
    name = 'Boulangerie Langlade'
    email = 'seller@mail.com'


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session
    name = 'baguette'
    description = 'classique'
    price = 0.68

    seller = factory.SubFactory(SellerFactory)
