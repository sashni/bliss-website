from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField, SelectField, FieldList, FormField
from wtforms.validators import InputRequired, Email
from wtforms import ValidationError

# Customer Action forms

class ContactForm(FlaskForm):
    first = StringField("First name: ", validators=[InputRequired()])
    last = StringField("Last name: ", validators=[InputRequired()])
    email = StringField("Email: ", validators=[InputRequired()])
    message = StringField("Enter message: ")
    submit = SubmitField("Submit")

class CheckoutForm(FlaskForm):
    first = StringField("First name:  ", validators=[InputRequired()])
    last = StringField("Last name: ", validators=[InputRequired()])
    email = StringField("Email: ", validators=[InputRequired()])
    phone = IntegerField("Phone: ", validators=[InputRequired()])
    message = StringField("Enter message: ")
    submit = SubmitField("Submit")

# Admin Action forms

# Register admin
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register Admin')


# Login/Register admin
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

    def check_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered, please log in')

# Add product to db
class addProduct(FlaskForm):
    gender = SelectField("Gender: ", choices=[('', ''), ('womens', 'Women'), ('mens', 'Men'), ('unisex', 'Unisex')], validators=[InputRequired()])
    category = SelectField("Category: ", choices=[], validators=[InputRequired()])
    name = StringField("Product name: ", validators=[InputRequired()])
    desc = StringField("Product description: ", validators=[InputRequired()])
    price = IntegerField("Price: ", validators=[InputRequired()])
    img = FileField(validators=[InputRequired()])
    active = BooleanField("In Stock")
    addproduct = SubmitField("Add Product")

class EditProduct(FlaskForm):
    product=IntegerField()
    editproduct = SubmitField("Update")

# View past orders
class getOrder(FlaskForm):
    order_id = IntegerField("Order ID")
    customer_email = StringField("Customer Email")
    getorder = SubmitField("View Orders")

class completeOrder(FlaskForm):
    submit = SubmitField("Order Completed")
