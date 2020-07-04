from lecopain.app import db

from lecopain.dao.models import (
    Seller, SellerSchema,
)

class SellerDao:

    @staticmethod
    def optim_read_all():

        # Create the list of people from our data

        all_sellers = Seller.query \
        .order_by(Seller.name) \
        .all()

        # Serialize the data for the response
        seller_schema = SellerSchema(many=True)
        return seller_schema.dump(all_sellers)
    
    @staticmethod
    def optim_read_all_pagination(page, per_page):

        # Create the list of people from our data

        all_sellers = Seller.query \
        .order_by(Seller.name) \
        .paginate(page=page, per_page=per_page)

        # Serialize the data for the response
        seller_schema = SellerSchema(many=True)
        return seller_schema.dump(all_sellers.items), all_sellers.prev_num, all_sellers.next_num
    
    @staticmethod
    def get_all():

        # Create the list of people from our data

        return Seller.query \
        .order_by(Seller.name) \
        .all()

    @staticmethod
    def get_one(id):
        # Create the list of people from our data
        return Seller.query.get_or_404(id)

    @staticmethod
    def read_one(id):
        # Create the list of people from our data
        seller = Seller.query.get_or_404(id)

        # Serialize the data for the response
        seller_schema = SellerSchema(many=False)
        return seller_schema.dump(seller)
