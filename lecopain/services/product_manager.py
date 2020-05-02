from lecopain.form import ProductForm
from lecopain.dao.models import Product
from lecopain import app, db

class ProductManager() :
    
    def update_product(self, form, product):
        productForm = Product(name=form.name.data, price=form.price.data, status=form.status.data, vendor_id=int(form.vendor_id.data), description=form.description.data)
        product.name = productForm.name
        product.status = productForm.status
        product.vendor_id = productForm.vendor_id
        product.description = productForm.description
        product.price = productForm.price

        db.session.commit()
        
    def convert_product_to_form(self, product, form) :
        form.vendor_id.data = product.vendor_id
        form.description.data = product.description
        form.status.data = product.status
        form.name.data = product.name
        form.price.data = product.price

        