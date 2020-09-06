from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

def strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value

def title_filter(value):
    if value is not None and hasattr(value, 'title'):
        return value.title()
    return value

class FlexibleDecimalField(DecimalField):

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(FlexibleDecimalField, self).process_formdata(valuelist)   

            


class PersonForm(FlaskForm):
    firstname = StringField('Prénom', validators=[
                            DataRequired(), Length(min=2, max=20)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    lastname = StringField('Nom', validators=[
                        DataRequired(), Length(min=2, max=20)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x)])
    address = StringField('Adresse', validators=[
                        DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x)])
    cp = StringField('Code Postal', validators=[
                        DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    city = StringField('Ville', validators=[
                        DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    submit = SubmitField('Valider')


class SellerForm(FlaskForm):
    name = StringField('Nom', validators=[
                    DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    city = StringField('Ville', validators=[
                    DataRequired(), Length(min=2, max=200)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x)])
    submit = SubmitField('Valider')
    
class UserForm(FlaskForm):
    username = StringField('Login', validators=[
                    DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x)])
    firstname = StringField('Prénom', validators=[
                    DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    lastname = StringField('Nom', validators=[
                    DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)] )
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=2, max=200)], filters=[lambda x: strip_filter(x)])
    password = PasswordField('Nouveau Mot de Passe', [
        DataRequired(), Length(min=6, max=30, message='Longueur minimale du Mot de passe : 6 caractères'),
        EqualTo('confirm', message='Les mots de passe doivent être identiques')])
    confirm = PasswordField('Confirmer le Mot de Passe ', validators=[DataRequired(), Length(min=6, max=30, message='Longueur minimale du Mot de passe : 6 caractères')])
    submit = SubmitField('Valider')

class PasswordForm(FlaskForm):
    password = PasswordField('Nouveau Mot de Passe', [
        DataRequired(), Length(min=6, max=30, message='Longueur minimale du Mot de passe : 6 caractères'),
        EqualTo('confirm', message='Les mots de passe doivent être identiques')])
    confirm = PasswordField('Confirmer le Mot de Passe ', validators=[DataRequired(), Length(min=6, max=30)])
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
    category_name = StringField('Catégorie')
    subscription_id = StringField('Id Abonnement')
    submit = SubmitField('Valider')

class ShippingDtForm(FlaskForm):
    title = StringField('Titre')
    shipping_dt = DateTimeField('Date de Livraison', format='%d/%m/%Y %H:%M:%S')
    submit = SubmitField('Valider')

class ProductForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()], filters=[lambda x: strip_filter(x), lambda x: title_filter(x)])
    short_name = StringField('Nom court', validators=[DataRequired()], filters=[lambda x: strip_filter(x)])
    price = FlexibleDecimalField('Prix')
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
    start_dt = DateTimeField('Date de debut', format='%d/%m/%Y')
    end_dt = DateTimeField('Date de fin', format='%d/%m/%Y')
    submit = SubmitField('Valider')

class SubscriptionDayForm(FlaskForm):
    category_name = StringField('Catégorie')
    submit = SubmitField('Valider')
    
