from flask import Blueprint, flash, jsonify, render_template, request, url_for, redirect, session
from flask_login import login_user, current_user, logout_user, login_required
from fitkit import db, bcrypt
from fitkit.product.routes import product
from fitkit.users.form import RegistrationForm, LoginForm, AddressForm
from fitkit.users.models import User, Cart, Order
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask_login import current_user, login_required
import razorpay
from sqlalchemy import or_
# from fitkit.config import 


# from fitkit.utils import generateOTP, send_Email
# key-id = rzp_test_VjLgQwIciQveWC
# key_secrect = DhDWNz9Q1Ta0YOeR3rmRlqoC

users = Blueprint('users', __name__,
                        template_folder='templates', static_folder='static')

RAZORPAY_KEY='rzp_test_VjLgQwIciQveWC'
RAZORPAY_SEC_ID='DhDWNz9Q1Ta0YOeR3rmRlqoC'
client = razorpay.Client(auth = (RAZORPAY_KEY, RAZORPAY_SEC_ID))

""" Add to cart """
@users.route("/addToCart", methods=['POST'])
# @login_required   # enable login required for production.
def addToCart():

    # user id saved in session
    # session['userid']


    p = request.form.get("p") # product_id
    s = request.form.get("s") # size selected
    q = request.form.get("q") # quantity

    print(p, q, s)

    if not p:
        flash(u"Product is required!", "danger")
        return redirect(url_for('product.detail'))

    if not s:
        flash(u"Select Size!", "danger")
        return redirect(url_for('product.detail', product_id=p))

    if not q:
        print("q not found")
        flash(u"Select Size!", "danger")
        return redirect(url_for('product.detail', product_id=p))


    """ after validation of all the required fields
        insert into database """
    current_user=1
    current_user = User.query.get_or_404(current_user)
    print(current_user)


    # item = Cart(quantity=q, size=s, product_id=current_user)
    
    item = Cart(quantity=q, size=s, product_id=p, cart_user=current_user)
    db.session.add(item)
    db.session.commit()

    
    flash(u"Item successfully added to the cart!", "success")
    return redirect("myCart")

""" My cart """
@users.route("/myCart")
# @login_required
def myCart():

    # remove this after login into the app.
    current_user = 1
    current_user = User.query.get_or_404(1)


    cart_items = Cart.query.filter_by(cart_user=current_user).all()
    print(111, cart_items)

    grandTotal = 0
    for product in cart_items:
        grandTotal = grandTotal + (product.product.price * product.quantity)

    print(len(cart_items), dir(cart_items))
    return render_template("users/myCart.html", cart_items=cart_items, grandTotal=grandTotal)


""" to a remove product from the cart """
@users.route("/removeFromCart")
# @login_required
def removeFromCart():

    cart_id = request.args.get("cart_id") # productid

    print(cart_id)
    if not cart_id:
       flash(u"Something went wrong!", "danger")
       return redirect("/myCart")
    
    # remove this after login into the app.
    current_user = 1
    current_user = User.query.get_or_404(1)


    cart_item = Cart.query.filter_by(id=cart_id, cart_user=current_user).all()
    print(111, current_user, cart_item)
    print(type(cart_item[0]))
    db.session.delete(cart_item[0])
    db.session.commit()

    flash(u"product Successfully removed from cart", "success")
    return redirect("myCart")



""" place-order route """
@users.route("/place_order", methods=["GET", "POST"])
# login_required
def placeOrder():

    form = AddressForm()

    if form.validate_on_submit():

        print("inside place_order post method")


        full_address = f"{form.name.data}\n{form.mob.data}\n\n{form.address.data} {form.city.data} {form.state.data}-{form.pincode.data}"
        print(full_address)

        session['address'] = full_address
        session['name'] = form.name.data
        session['mob'] = form.mob.data

        print(session['address'], session['mob'], session['name'])
        return redirect(url_for('users.checkout'))
        
    return render_template("users/add_address.html", form=form)


@users.route("/checkout")
# @login_required
def checkout():


    if 'name' not in session or 'mob' not in session or 'address' not in session:
        return redirect(url_for('users.placeOrder'))


    address = session['address']
    name = session['name']
    mob = session['mob']
    
    print("Payment Successfull", "success")
    current_user = 1
    current_user = User.query.get_or_404(1)

    cart_items = Cart.query.filter_by(cart_user=current_user).all()
    print(111, cart_items)

    grandTotal = 0
    for product in cart_items:
        grandTotal = grandTotal + (product.product.price * product.quantity)


    if grandTotal == 0:
        flash(u"Cart is Empty", "danger")
        return redirect("/myCart")

    ''' creating order '''
    

    data = {
            'amount': grandTotal * 100,
            "currency" : "INR",
            "receipt" : 'razorpaydemo'
        }
    razorpay_order = client.order.create(data = data)
    print(razorpay_order)



    user = User.query.filter_by(id=current_user.id).all()
    print(user[0])
    
    return render_template("users/payment.html", address=address, name=name, mob=mob, email=user[0].email, order=razorpay_order, key_id=RAZORPAY_KEY)


@users.route("/verify_payment", methods=['POST'])
def verifyPayment():
    
    payment_id = request.form.get("razorpay_payment_id")
    order_id = request.form.get("razorpay_order_id")
    signature = request.form.get("razorpay_signature")
    add = request.form.get('address')
    print(1111, add)

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        return redirect(url_for('users.closeOrder'))
    except razorpay.errors.SignatureVerificationError:
        return "Signature verification failed", 400


@users.route('/close_order')
def closeOrder():
    print('this is close order route')
    current_user = 1
    current_user = User.query.get_or_404(1)

    address = session['address']


    cart_items = Cart.query.filter_by(cart_user=current_user).all()

    for item in cart_items:
        print(item.id, item.cart_user, item)
        o = Order(address=address, 
                  order_size=item.size, order_quantity=item.quantity, product=item.product, order_user=current_user)
        
        db.session.add(o)
        db.session.delete(item)
    
    db.session.commit()
    print('your order has been placed')
    return redirect(url_for('users.myOrders')) # change it to users.myOrders

""" my orders """
@users.route("/my_orders")
# @login_required
def myOrders():

    current_user = 1
    current_user = User.query.get_or_404(current_user)

    latest_orders = Order.query.filter(or_(Order.order_status=='Dispatched', Order.order_status=='Booked'), Order.order_user==current_user).all()

    shipped_orders = Order.query.filter_by(order_user=current_user, order_status='Completed').all()
    

    return render_template("users/myOrders.html", latest_orders=latest_orders, completed_orders=shipped_orders)
    

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("InternalServerError.html", error=e.name, code = e.code)


# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)




""" login """
@users.route("/login", methods=['GET', 'POST'])
def login():


    if current_user.is_authenticated:
        return redirect(url_for('product.index'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




""" new user registration """
@users.route("/registration", methods=["POST", "GET"])
def registration():

    form = RegistrationForm()  
    if form.validate_on_submit():     
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template("registration.html", form=form)


@users.route("/registerUser", methods=["POST"])
def registerUser():

    email = request.form.get("email")
    password = request.form.get("pass")


    # hashing the password
    hash = generate_password_hash(password)

    # insert the data into database
    with db_connection:
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("INSERT INTO users (email, hash) VALUES (%s, %s)",(email, hash))


    session.clear()

    # Query database for the user
    with db_connection:
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT user_id FROM users WHERE email = %s;", (request.form.get("email"),))
            rows = cursor.fetchall()


    # Remember which user has logged in
    session["user_id"] = rows[0]["user_id"]

    # flashing the success message to the next route with category as 'success'
    flash(u"User Successfully Registered!", "success")

    # Redirect user to home page
    return redirect("/")


@users.route("/forgotPassword", methods=["GET", "POST"])
def forogtpassword():
    """changing user's password"""

    with db_connection:
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (request.form.get("email"),))
            users = cursor.fetchall()


        return render_template("/users/forgot_password.html")



@users.route("/otp", methods=["POST"])
def otp():

    if not request.form.get('otp'):

        return jsonify(
                {
                    "status" : "error",
                    "message" : "Otp Missing"
                })

    elif session["otp"] != request.form.get('otp'):

        session['otp'] = generateOTP(session["email"])
        return jsonify(
                {
                    "status" : "error",
                    "message" : "Invalid Otp!"
                })

    else:
        session.pop('otp')
        return jsonify(
                {
                    "status" : "success",
                    "message" : "Otp Matched"
                })


@users.route("/reset_password", methods=["POST"])
def reset_password():

    if not request.form.get('newPassword'):

        return jsonify(
                {
                    "status" : "error",
                    "message" : "password missing!"
                })

    if not request.form.get('confirmPassword'):

        return jsonify(
                {
                    "status" : "error",
                    "message" : "confirm your password!"
                })

    if not request.form.get('newPassword') == request.form.get('confirmPassword'):

        return jsonify(
                {
                    "status" : "error",
                    "message" : "password didn't matched!"
                })

    else:
        # hashing the new password
        hash = generate_password_hash(request.form.get("newPassword"))

        # update the new hashed password into database
        with db_connection:
            with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("UPDATE users SET hash = %s WHERE email = %s", (hash, session["email"],))
                users = cursor.fetchall()


        # forget the user's logging
        session.clear()

        # flashing the message of successful changed password
        flash(u"Password successfully changed!", "success")

        return jsonify(
                {
                    "status" : "success",
                    "message" : ""
                })




""" route for loggin out """
@users.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


