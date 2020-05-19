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
    def get_category_from_lines(lines):

        id = lines[0].get('product_id')
        # Create the list of people from our data
        product = Product.query.get_or_404(id)

        return product.category
