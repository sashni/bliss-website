import os
from bliss import basedir
from flask import Blueprint, render_template, redirect, request, url_for, flash, session, jsonify
from bliss import db
from bliss.models import Product, Customer, Order, OrderItem, Admin
from bliss.forms import addProduct, EditProduct, RegisterForm, LoginForm, getOrder, completeOrder
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
import base64

bp = Blueprint('admin', __name__)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('store.index'))

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        admin = Admin.query.filter_by(email=form.email.data).first()

        if admin is not None and admin.check_password(password=form.password.data):
            login_user(admin, remember=True)

            next = url_for('admin.list')

            return redirect(next)

    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin(email=form.email.data, password=form.password.data)
        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('admin.login'))

    return render_template('login.html', form=form)

# Get categories of gender
@bp.route('/categories/<g>')
@login_required
def getCategories(g):
    products = Product.query.filter_by(gender=g).with_entities(Product.category).distinct().all()
    categoryArray = []
    print(products)
    for p in products:
        categoryArray.append(p[0])
    return jsonify({'categories': categoryArray})

# Delete product from db
@bp.route('/delete/<pid>')
@login_required
def delete(pid):
    product = Product.query.get(pid)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin.list'))

# Admin View of Products, Add product to db
@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def list():
    addform = addProduct()
    orderform = getOrder()
    womens = Product.query.filter_by(gender='womens').order_by('category').all()
    mens = Product.query.filter_by(gender='mens').order_by('category').all()
    unisex = Product.query.filter_by(gender='unisex').order_by('category').all()
    addform.category.choices = [(addform.category.data, addform.category.data)]
    orders = []

    if addform.validate_on_submit():
        gender = (addform.gender.data).lower()
        category = (addform.category.data).lower()
        name = addform.name.data
        desc = addform.desc.data
        price = addform.price.data
        img = base64.b64encode(addform.img.data.read()).decode('utf-8')
        active = addform.active.data
        if category == 'other':
          category = ' '.join(request.form.get('otherCategory').lower().split())
        print(category)
        new_product = Product(gender,category,name,desc,price,img,active)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin.list'))

    elif request.method == "POST":
        order_id = orderform.order_id.data
        customer_email = orderform.customer_email.data

        if order_id:
          order = Order.query.get(order_id)
          if order == None:
            flash(f'Order {order_id} does not exist')
          else:
            return(url_for('admin.order', order_id=order_id))
          orders = [order]
        elif customer_email:
          orders = Order.query.filter_by(customer_email=customer_email).all()
          if len(orders) == 0:
            flash(f'Customer {customer_email} does not exist')
          else:
            return(url_for('admin.order', order_id=customer_email))

    return render_template('admin.html', womens=womens, mens=mens, unisex=unisex, addform=addform, orderform=orderform, orders=orders)

@bp.route('/admin/order/<order_id>', methods=['GET', 'POST'])
@login_required
def order(order_id):
    orders = []
    try:
        orders.push(Order.query.get(int(order_id)))
    except:
        orders = Order.query.filter_by(customer_email=order_id).all()
    return render_template('adminorder.html', orders=orders)

# Get Customer Info
@bp.route('/customer/<customer_email>')
@login_required
def getCustomer(customer_id):
    customer = Customer.query.get(customer_email)
    customerObj = {
      'email': customer.email,
      'first': customer.first,
      'last': customer.last,
      'phone': customer.phone
    }
    return jsonify({'customer': customerObj})
