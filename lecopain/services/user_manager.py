from lecopain.app import app, db
from lecopain.dao.models import User
from lecopain.dao.user_dao import UserDao


class userManager():

    def optim_get_all(self):
        return UserDao.optim_read_all()
    
    def optim_get_all_pagination(self, role_name=all, page=1, per_page=10):
        return UserDao.optim_read_all_role_pagination(role_name, page, per_page)
    
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
        
