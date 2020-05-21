from lecopain.app import app, db
from lecopain.dao.models import Order, Seller
from lecopain.dao.seller_dao import SellerDao


class SellerManager():

    def optim_get_all(self):
        return SellerDao.optim_read_all()
