from lecopain.app import db

from lecopain.dao.models import (
    Role, RoleSchema,
)

class RoleDao:

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_roles = Role.query \
        .order_by(Role.name) \
        .all()

        # Serialize the data for the response
        role_schema = RoleSchema(many=True)
        return role_schema.dump(all_roles)
    
    @staticmethod
    def get_all():
        # Create the list of people from our data
        return Role.query \
        .order_by(Role.name) \
        .all()



    @staticmethod
    def read_one(id):
        # Create the list of people from our data
        role = Role.query.get_or_404(id)

        # Serialize the data for the response
        role_schema = RoleSchema(many=False)
        return role_schema.dump(role)
    
    @staticmethod
    def get_one(id):
        # Create the list of people from our data
        return Role.query.get_or_404(id)
