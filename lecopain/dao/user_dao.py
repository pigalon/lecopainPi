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
    def optim_read_all_role_pagination(role_id, page, per_page):

        # Create the list of people from our data
        print('role_id : ' + str(role_id))

        if role_id != 0:
            all_users = User.query.join(UserRoles, UserRoles.user_id == User.id).join(Role, UserRoles.role_id == Role.id)
            all_users = all_users.filter(Role.id == role_id)
        else:
            all_users = User.query
            
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
    def get_by_username(username):
        # Create the list of people from our data
        return User.query.filter(User.username == username).first()


    @staticmethod
    def read_one(id):
        # Create the list of people from our data
        user = User.query.get_or_404(id)

        # Serialize the data for the response
        user_schema = UserSchema(many=False)
        return user_schema.dump(user)
