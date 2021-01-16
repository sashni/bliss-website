from bliss import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(admin_id)

class Admin(db.Model, UserMixin):
    __tablename__ = 'Admins'
    email = db.Column(db.String(64), primary_key=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Admin: {self.email}"

    def get_id(self):
        return self.email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    category = db.Column(db.Text)
    name = db.Column(db.Text)
    desc = db.Column(db.Text)
    price = db.Column(db.Integer)
    img = db.Column(db.Text)
    active = db.Column(db.Boolean)

    def __init__(self, gender, category, name, desc, price, img, active):
        self.gender = gender
        self.category = category
        self.name = name
        self.desc = desc
        self.price = price
        self.img = img
        self.active = active

    def __repr__(self):
        return f"Product: {self.name}, Gender: {self.gender}, Category: {self.category}, Description: {self.desc}, Price: {self.price}, Active: {self.active}"

class OrderItem(db.Model):
    __tablename__ = 'OrderItems'
    item_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'))
    quantity = db.Column(db.Integer)

    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = self.product_id
        self.quantity = quantity

    def __repr__(self):
        return f"Order id: {self.order_id}, Product id: {self.product_id}, Quantity: {self.quantity}"

    def change_quantity(self, quantity):
        self.quantity = quantity

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.Text, db.ForeignKey('Customers.email'))
    date = db.Column(db.Date)
    # one to many
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __init__(self, email, date):
        self.customer_email = email
        self.date = date

    def __repr__(self):
        return f"Order id: {self.order_id} \n Customer: {self.customer_email} \n Products: {self.items}"

    def get_products(self):
      for item in self.items:
        print(item.product_id, item.quantity)

class Customer(db.Model):
    __tablename__ = 'Customers'
    email = db.Column(db.Text, primary_key=True)
    first = db.Column(db.Text)
    last = db.Column(db.Text)
    phone = db.Column(db.Integer)
    # one to many
    orders = db.relationship('Order', backref="customer", lazy='dynamic')

    def __init__(self, email, first, last, phone):
        self.email = email
        self.first = first
        self.last = last
        self.phone = phone

    def __repr__(self):
        return f"Name: {self.first} {self.last}, Email: {self.email}, Phone: {self.phone}"
