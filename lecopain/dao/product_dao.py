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

      all_products =  all_products.order_by(Product.name.asc()).all()

      # Serialize the data for the response
      product_schema = ProductSchema(many=True)
      return product_schema.dump(all_products)
  
  @staticmethod
  def read_all_by_seller_pagination(seller_id, page, per_page):

      # Create the list of people from our data

      all_products = Product.query
      if seller_id !=0 :
          all_products = all_products.filter(
              Product.seller_id == seller_id)

      all_products =  all_products.order_by(Product.name.asc())\
      .paginate(page=page, per_page=per_page)

      # Serialize the data for the response
      product_schema = ProductSchema(many=True)
      return product_schema.dump(all_products.items), all_products.prev_num, all_products.next_num

  @staticmethod
  def read_all_by_seller_category(seller_id, category):
      # Create the list of people from our data

      all_products = Product.query
      if seller_id !=0 :
          all_products = all_products.filter(
              Product.seller_id == seller_id)

          all_products = all_products.filter(
              Product.category == category)

      all_products = all_products.order_by(Product.name.asc()).all()

      # Serialize the data for the response
      product_schema = ProductSchema(many=True)
      return product_schema.dump(all_products)

  @staticmethod
  def create(product):
    created_product = Product(name=product.get('name'),
      short_name=product.get('short_name'),
      seller_id=product.get('seller_id'),
      price=product.get('price'),
      description=product.get('description'),
      category=product.get('category'), status='DISPONIBLE')

    db.session.add(created_product)
    db.session.commit()

  # @
  #
  @staticmethod
  def count_by_seller(seller_id):
    return Product.query \
      .filter(Product.seller_id == seller_id) \
      .order_by(Product.name.asc()) \
      .count()