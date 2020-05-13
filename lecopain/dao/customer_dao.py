from lecopain.app import db

from lecopain.dao.models import (
    Customer, CustomerSchema,
    OptimizedCustomerSchema,
)

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
    def read_one(id):

        # Create the list of people from our data
        customer = Customer.query.get_or_404(id)

        # Serialize the data for the response
        customer_schema = CustomerSchema(many=False)
        return customer_schema.dump(customer)
