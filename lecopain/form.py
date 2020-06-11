from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class PersonForm(FlaskForm):
    firstname = StringField('Prénom', validators=[
                            DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Nom', validators=[
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
    name = StringField('Nom', validators=[
                       DataRequired(), Length(min=2, max=200)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Valider')


class OrderForm(FlaskForm):
    title = StringField('Titre')
    customer_id = IntegerField('Client Id:', validators=[DataRequired()])
    seller_id = IntegerField('Vendeur Id:')
    shipping_dt = DateTimeField('Date de Livraison', format='%d/%m/%Y')
    status = StringField('Status')
    submit = SubmitField('Valider')

class ShipmentForm(FlaskForm):
    title = StringField('Titre')
    customer_id = IntegerField('Client Id:', validators=[DataRequired()])
    shipping_dt = DateTimeField('Date de Livraison', format='%d/%m/%Y')
    status = StringField('Status')
    submit = SubmitField('Valider')


class ShippingDtForm(FlaskForm):
    title = StringField('Titre')
    shipping_dt = DateTimeField('Date de Livraison', format='%d/%m/%Y %H:%M:%S')
    submit = SubmitField('Valider')


class ProductForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    short_name = StringField('Nom court', validators=[DataRequired()])
    price = DecimalField('Prix')
    description = StringField('Description')
    seller_id = IntegerField('Vendeur Id:', validators=[DataRequired()])
    category = StringField('Catégorie')
    submit = SubmitField('Valider')


class ShippingForm(FlaskForm):
    reference = StringField('Référence', validators=[DataRequired()])
    order_id = IntegerField(
        'Commande Id:', validators=[DataRequired()])
    shipping_dt = DateTimeField('Date de Livraison')
    status = StringField('Statut')
    submit = SubmitField('Valider')


class CancellationForm(FlaskForm):
    submit = SubmitField('Annulation')


class LoginForm(FlaskForm):
    username = StringField('Login')
    password = PasswordField('Mot de Passe')
    submit = SubmitField('Envoyer')


class SubscriptionForm(FlaskForm):
    customer_id = IntegerField('Client Id:', validators=[DataRequired()])
    seller_id = IntegerField('Vendeur Id:', validators=[DataRequired()])
    start_dt = DateTimeField('Date de debut', format='%d/%m/%Y')
    end_dt = DateTimeField('Date de fin', format='%d/%m/%Y')
    submit = SubmitField('Valider')
    

class SubscriptionDayForm(FlaskForm):
    submit = SubmitField('Valider')
