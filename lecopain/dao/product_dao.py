from lecopain.app import db

from lecopain.dao.models import (
    Product, ProductSchema,
    OptimizedProductSchema,
)

class ProductDao:

    @staticmethod
    def optim_read_all():
        # Create the list of people from our data
        all_products = Product.query \
        .order_by(Product.name) \
        .all()
        # Serialize the data for the response
        product_schema = OptimizedProductSchema(many=True)
        return product_schema.dump(all_products)

    @staticmethod
    def read_all():
        # Create the list of people from our data
        all_products = Product.query \
            .order_by(Product.name) \
            .all()
        # Serialize the data for the response
        product_schema = ProductSchema(many=True)
        return product_schema.dump(all_products)

    @staticmethod
    def read_one(id):
        # Create the list of people from our data
        product = Product.query.get_or_404(id)
        # Serialize the data for the response
        product_schema = ProductSchema(many=False)
        return product_schema.dump(product)

    @staticmethod
    def get_one(id):
        return Product.query.get_or_404(id)

    @staticmethod
    def read_all_by_seller(seller_id):

        # Create the list of people from our data

        all_products = Product.query
        if seller_id !=0 :
            all_products = all_products.filter(
                Product.seller_id == seller_id)

        all_products.order_by(Product.name).all()

        # Serialize the data for the response
        product_schema = ProductSchema(many=True)
        return product_schema.dump(all_products)

