from lecopain.app import app, db
from lecopain.dao.models import Order, Seller
from lecopain.dao.seller_dao import SellerDao


class SellerManager():

    def optim_get_all(self):
        return SellerDao.optim_read_all()
    
    def optim_get_all_pagination(self, page=1, per_page=10):
        return SellerDao.optim_read_all_pagination(page, per_page)

    def read_one(self,  seller_id):
        return SellerDao.read_one(seller_id)
    
    def get_one(self,  seller_id):
        return SellerDao.get_one(seller_id)
