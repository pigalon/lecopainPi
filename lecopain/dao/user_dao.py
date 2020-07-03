from lecopain.app import db

from lecopain.dao.models import (
    User, UserSchema, Role, UserRoles
)

class UserDao:

    @staticmethod
    def optim_read_all():

        # Create the list of people from our data

        all_users = User.query \
        .order_by(User.username) \
        .all()

        # Serialize the data for the response
        user_schema = UserSchema(many=True)
        return user_schema.dump(all_users)
    
    @staticmethod
    def optim_read_all_role_pagination(role_name, page, per_page):

        # Create the list of people from our data

        all_users = User.query.join(UserRoles, UserRoles.user_id == User.id).join(Role, UserRoles.role_id == Role.id)
        
        if role_name != 'all':
            all_users = all_users.filter(Role.name == role_name)
            
        all_users = all_users.order_by(User.username) \
        .paginate(page=page, per_page=per_page)
        
        

        # Serialize the data for the response
        user_schema = UserSchema(many=True)
        return user_schema.dump(all_users.items), all_users.prev_num, all_users.next_num
    
    @staticmethod
    def get_all():

        # Create the list of people from our data

        return User.query \
        .order_by(User.name) \
        .all()
        
    @staticmethod
    def get_one(id):
        # Create the list of people from our data
        return User.query.get_or_404(id)



    @staticmethod
    def read_one(id):
        # Create the list of people from our data
        user = User.query.get_or_404(id)

        # Serialize the data for the response
        user_schema = UserSchema(many=False)
        return user_schema.dump(user)
