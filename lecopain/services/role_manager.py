from lecopain.app import app, db
from lecopain.dao.models import Role
from lecopain.dao.role_dao import RoleDao


class roleManager():

    def read_all(self):
        return RoleDao.read_all()
    
    def read_one(self,  role_id):
        return RoleDao.read_one(role_id)

    def get_all(self):
        return RoleDao.get_all()
    
    def get_one(self,  role_id):
        return RoleDao.get_one(role_id)
