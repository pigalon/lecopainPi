from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class PersonForm(FlaskForm):
    firstname = StringField('firstName', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('LastName', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Add person')

class OrderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    customer_id = IntegerField('Customer Id:', validators=[DataRequired()])
    product_id = IntegerField('Product Id:', validators=[DataRequired()])
    order_dt = DateTimeField('Order Date')
    submit = SubmitField('Add order')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price')
    description = StringField('Description')
    submit = SubmitField('Add product')