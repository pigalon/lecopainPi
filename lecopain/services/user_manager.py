from lecopain.app import app, db
from lecopain.dao.models import User, Role
from lecopain.dao.user_dao import UserDao
from lecopain.dao.role_dao import RoleDao
from datetime import datetime


class userManager():

    def optim_get_all(self):
        return UserDao.optim_read_all()
    
    def optim_get_all_pagination(self, role_id=0, page=1, per_page=10):
        return UserDao.optim_read_all_role_pagination(role_id, page, per_page)
    
    def get_one(self,  user_id):
        return UserDao.get_one(user_id)
    
    def read_one(self,  user_id):
        return UserDao.read_one(user_id)
    
    def active(self, user_id):
        user = self.get_one(user_id)
        user.set_active()
        db.session.commit()
    
    def deactivate(self, user_id):
        user = self.get_one(user_id)
        user.set_inactive()
        db.session.commit()
        
    def change_password(self, user_id, password):
        user = self.get_one(user_id)
        user.set_password(password)
        db.session.commit()
        
    def change_role(self, user_id, role, account_id):
        user = self.get_one(user_id)
        user.roles = [role,]
        if account_id is not None and account_id > 0:
            user.account_id = account_id
        db.session.commit()
        
    def create(self, form):
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    firstname=form.firstname.data,
                    lastname=form.lastname.data)
        user.set_password(form.password.data)
        user.joined_at = datetime.today()
        user.set_active()
        db.session.add(user)
        db.session.commit()
        role = RoleDao.get_one_from_name('user_role')
        user.roles.append(role)
        db.session.commit()
        
    def update(self, user, form):
        user.username = form.username.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.email = form.email.data

        db.session.commit()
        
    def delete(self, user_id):
        user = UserDao.get_one(user_id)
        db.session.delete(user)
        db.session.commit()

        
