from lecopain.app import app, db
from lecopain.dao.models import User
from lecopain.dao.user_dao import UserDao


class userManager():

    def optim_get_all(self):
        return UserDao.optim_read_all()
    
    def optim_get_all_pagination(self, role_name=all, page=1, per_page=10):
        return UserDao.optim_read_all_role_pagination(role_name, page, per_page)

    def get_one(self,  user_id):
        return UserDao.read_one(user_id)
