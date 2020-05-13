from lecopain.app import db

from lecopain.dao.models import (
    Customer,
    CustomerSchema,
)

class CustomerDao:

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_customers = Customer.query \
        .order_by(Customer.lastname) \
        .all()

        # Serialize the data for the response
        customer_schema = CustomerSchema(many=True)
        return customer_schema.dump(all_customers)
