import os
from threading import Thread
from flask import (
    Blueprint, flash, g, redirect, session, render_template, request, url_for, current_app, jsonify
)
#from flask_mail import Message
from bliss import db#, mail
from bliss.models import Product, Order, OrderItem, Customer
from bliss.forms import ContactForm, CheckoutForm
from datetime import date

bp = Blueprint('store', __name__)

@bp.route('/')
def index():
    session.modified = True
    if 'cart' not in session:
        session['cart'] = {}
    products = Product.query.all()
    return render_template('index.html', products=products)

@bp.route('/<filter>', methods=['GET', 'POST'])
def products(filter):
    # TO DO: Redirect to page not found if filter not valid
    filters = filter.split("-")
    products = categories = []
    try:
      (gender, category) = (filters[0], filters[1:])
      print(gender, category)
      if (len(category) > 0):
        category = ' '.join(category)
      print(category)

      if (gender == "womens" or gender == "mens" or gender == "unisex"):
        if (len(category) == 0):
          products = Product.query.filter_by(gender=gender).all()
        else:
          products = Product.query.filter_by(gender=gender, category=category).all()
      print(products)
      if (len(products) == 0):
        raise Exception()


      categoryArray = Product.query.filter_by(gender=gender).with_entities(Product.category).distinct().all()
      categories = [c[0] for c in categoryArray]
      print(categories)
    except:
      pass
    #return redirect(url_for('store.page_not_found'))
    return render_template('products.html', products=products, categories=categories, gender=gender.capitalize(), category=category)


@bp.route('/products/<product_id>/<admin>')
def product(product_id, admin):
    product = Product.query.get(product_id)
    return render_template('product.html', product=product, admin=admin)

@bp.route('/cart/<product_id>')
def add_to_cart(product_id):
    print('add to cart')
    print(session)
    session.modified = True
    if "cart" in session:
        quantity = session['cart'].get(product_id, 0)
        session['cart'][product_id] = quantity + 1
    else:
        session["cart"] = {product_id:1}
        print(session)

    product = Product.query.get(product_id)

    return redirect(url_for('store.products', g='all', c='all'))

def send_async_email(app, msg):
    with app.app_context():
        try:
            print("Send email")
            #mail.send(msg)
        except Exception as e:
            raise e


def send_email(customer, products, order_id, message):
    # CHANGE HOST WHEN DEPLOYED
    host = "http://127.0.0.1:5000"

    # Send Email to Customer
    msg = Message(f"Thank You for Your Order Inquiry #{order_id}", recipients=[customer.email])
    msg.html = render_template('mail.html', products=products, customer=customer, message=message, host=host, ToCustomer=True)
    Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()

    # Send Email to Admin
    #msg = Message(f"New Order Inquiry #{order_id}", recipients=[current_app.config["MAIL_DEFAULT_SENDER"]])
    #msg.html = render_template('mail.html', products=products, customer=customer, host=host, ToCustomer=False)
    #Thread(target=send_async_email,
    #           args=(current_app._get_current_object(), msg)).start()

@bp.route('/cart/', methods=['GET','POST'])
def view_cart():
    form = CheckoutForm()
    products = {}
    for p_id, quantity in session['cart'].items():
        products[Product.query.get(p_id)] = quantity

    if form.validate_on_submit():
        # create new order
        order = Order(date.today())
        # Get inputted text quantities
        # Add products and quantities to order
        quantities = request.form.getlist('quantity')
        order_products = []
        order_quantities = []
        for ((product, quantity), new_quantity) in zip(products.items(), quantities):
            products[product] = int(new_quantity)
            order.products.append(product)
            order.quantities.append(Quantity(order.order_id, product.product_id, new_quantity))
        order.message = form.message.data
        db.session.add(order)
        db.session.commit()

        # Add Order to Customer
        customer = Customer.query.get(form.email.data)
        if customer is None:
            customer = Customer(form.first.data, form.last.data, form.email.data, form.phone.data)
            customer.orders.append(order)
            db.session.add(customer)
        else:
            customer.first = form.first.data
            customer.last = form.last.data
            customer.phone = form.phone.data
            customer.orders.append(order)
            db.session.add(customer)

        db.session.commit()
        print(order.order_id)

        send_email(customer=customer, products=products, order_id=order.order_id, message=order.message)
        session['cart'] = {}
        flash(f"{form.email.data}")
        return redirect(url_for('store.view_cart'))

    return render_template('order.html', products=products, form=form)

@bp.route('/cart/remove/<product_id>')
def remove_from_cart(product_id):
    del session['cart'][product_id]
    print('removed', session['cart'])
    return redirect(url_for('store.view_cart'))

@bp.route('/contact')
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        first = form.first.data
        last = form.last.data
        email = form.email.data
        message = form.message.data

        # Send Email to Admin
        msg = Message(f"New Cusomter Message", recipients=[current_app.config["MAIL_DEFAULT_SENDER"]])
        # TO DO: render contact email html file
        #msg.html = render_template('mail.html', products=products, quantities=quantities, customer=customer, host=host, ToCustomer=False)
        Thread(target=send_async_email,
                   args=(current_app._get_current_object(), msg)).start()

    return render_template('contact.html', form=form)

@bp.route('/404')
def page_not_found():
    return render_template('404.html')
