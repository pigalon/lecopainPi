from lecopain.form import ProductForm
from lecopain.dao.models import Product
from lecopain.app import app, db
from lecopain.dao.product_dao import ProductDao


class ProductManager():

    def update_product(self, form, product):
        productForm = Product(name=form.name.data, price=form.price.data, status=form.status.data, seller_id=int(
            form.seller_id.data), description=form.description.data)
        product.name = productForm.name
        product.status = productForm.status
        product.seller_id = productForm.seller_id
        product.description = productForm.description
        product.price = productForm.price

        db.session.commit()

    def convert_product_to_form(self, product, form):
        form.seller_id.data = product.seller_id
        form.description.data = product.description
        form.status.data = product.status
        form.name.data = product.name
        form.price.data = product.price
        
    def get_all(self):
        return ProductDao.read_all()

    def optim_get_all(self):
        return ProductDao.optim_read_all()

    def get_one(self, id):
        return ProductDao.read_one(id)

    def get_category_from_lines(self, lines):
        id = lines[0].get('product_id')
        product = ProductDao.get_one(id)
        return product.category
