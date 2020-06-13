from lecopain.app import db

from lecopain.dao.models import (
    Customer, CustomerSchema,
    OptimizedCustomerSchema,
)
from sqlalchemy import func

class CustomerDao:

    @staticmethod
    def optim_read_all():

        # Create the list of people from our data

        all_customers = Customer.query \
        .order_by(Customer.lastname) \
        .all()

        # Serialize the data for the response
        customer_schema = OptimizedCustomerSchema(many=True)
        return customer_schema.dump(all_customers)

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_customers = Customer.query \
            .order_by(Customer.lastname) \
            .all()

        # Serialize the data for the response
        customer_schema = CustomerSchema(many=True)
        return customer_schema.dump(all_customers)

    @staticmethod
    def read_all_by_cities(city):

        # Create the list of people from our data

        all_customers = Customer.query

        if city != 'all' :
            all_customers = all_customers.filter(func.lower(Customer.city) == func.lower(city)) 
        
        all_customers = all_customers.order_by(Customer.firstname).all()

        # Serialize the data for the response
        customer_schema = CustomerSchema(many=True)
        return customer_schema.dump(all_customers)

    @staticmethod
    def read_one(id):

        # Create the list of people from our data
        customer = Customer.query.get_or_404(id)

        # Serialize the data for the response
        customer_schema = CustomerSchema(many=False)
        return customer_schema.dump(customer)

    @staticmethod
    def get_all_cities():

        # Create the list of people from our data

        cities = Customer.query.with_entities(Customer.city).distinct(Customer.city).all()
        final_cities = []
        for city in cities:
            final_cities.append(city[0])
        return final_cities
