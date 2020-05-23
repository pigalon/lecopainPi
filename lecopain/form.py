from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class PersonForm(FlaskForm):
    firstname = StringField('firstName', validators=[
                            DataRequired(), Length(min=2, max=20)])
    lastname = StringField('LastName', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=2, max=200)])
    address = StringField('Adresse', validators=[
                          DataRequired(), Length(min=2, max=200)])
    cp = StringField('Code Postal', validators=[
                     DataRequired(), Length(min=2, max=200)])
    city = StringField('Ville', validators=[
                       DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Valider')


class SellerForm(FlaskForm):
    name = StringField('name', validators=[
                       DataRequired(), Length(min=2, max=200)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Valider')


class OrderForm(FlaskForm):
    title = StringField('Title')
    customer_id = IntegerField('Customer Id:', validators=[DataRequired()])
    seller_id = IntegerField('Seller Id:')
    shipping_dt = DateTimeField('Shipping Date', format='%d/%m/%Y')
    status = StringField('Status')
    submit = SubmitField('Valider')

class OrderShippingDtForm(FlaskForm):
    title = StringField('Title')
    shipping_dt = DateTimeField('Shipping Date', format='%d/%m/%Y %H:%M:%S')
    submit = SubmitField('Valider')


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price')
    description = StringField('Description')
    seller_id = IntegerField('Seller Id:', validators=[DataRequired()])
    status = StringField('Status')
    submit = SubmitField('Valider')


class ShippingForm(FlaskForm):
    reference = StringField('Reference', validators=[DataRequired()])
    order_id = IntegerField(
        'Customer Order Id:', validators=[DataRequired()])
    shipping_dt = DateTimeField('Order Date')
    order_id = IntegerField(
        'Customer Order Id:', validators=[DataRequired()])
    status = StringField('Status')
    submit = SubmitField('Valider')


class OrderAnnulationForm(FlaskForm):
    submit = SubmitField('Annulation')


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class SubscriptionForm(FlaskForm):
    customer_id = IntegerField('Customer Id:', validators=[DataRequired()])
    seller_id = IntegerField('Seller Id:', validators=[DataRequired()])
    start_dt = DateTimeField('Date de debut', format='%d/%m/%Y')
    end_dt = DateTimeField('Date de fin', format='%d/%m/%Y')
    submit = SubmitField('Valider')
    

class SubscriptionDayForm(FlaskForm):
    submit = SubmitField('Valider')
