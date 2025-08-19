from flask import Blueprint, flash, jsonify, render_template, current_app, request, url_for, redirect, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from fitkit.utils import generateOTP, send_Email, upload_img, remove_img
from functools import wraps
from flask_login import current_user
from fitkit import db
from fitkit.config import Config
from fitkit.users.routes import login

from fitkit.users.models import Order
from fitkit.product.models import Product
from fitkit.admin.forms import ProductForm

import secrets

ADMIN_LOGIN_ID=Config.ADMIN_LOGIN_ID
ADMIN_LOGIN_PASS=Config.ADMIN_LOGIN_PASS

admin = Blueprint('admin', __name__,
                        template_folder='templates', static_folder='static')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.url)
        if not current_user.is_authenticated or current_user.role != 'admin':
            return redirect(url_for('users.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



""" admin dashboard """
@admin.route("/dashboard", methods=["GET", "POST"])
@admin.route("/", methods=["GET", "POST"])
@admin_required     # to confirm that admin is logged-in and not a user
def dashboard():
    # print(secrets.token_hex(8))
    return render_template("admin/dashboard.html")

@admin.route("/orders")
# @admin_required  
def orders():
    latestOrders = Order.query.filter_by(order_status='Booked').all()  # Assuming 'Booked' means new orders
    dispatchedOrders = Order.query.filter_by(order_status='Dispatched').all()
    print(len(latestOrders), len(dispatchedOrders))
    return render_template("admin/orders.html", latest_orders=latestOrders, in_transit_orders=dispatchedOrders)


@admin.route("/dispatch_order")
@admin_required  
def dispatchOrder():
    p = request.args.get('p')
    order = Order.query.filter_by(id=p).first()
    print(p, order)
    if order.order_status == 'Booked':
        order.order_status = 'Dispatched'  # Update the order status to 'Dispatched'
        db.session.commit()
        flash("Order dispatched successfully", "success")  
    else:
        flash("Order is not in a state to be dispatched", "danger")

    # Redirect to the orders page after dispatching the order 
    return redirect(url_for('admin.orders'))


@admin.route("/complete_order")
@admin_required       
def completeOrder():
    p = request.args.get('p')
    order = Order.query.filter_by(id=p).first()
    if order.order_status == 'Dispatched':
        order.order_status = 'Completed'  # Update the order status to 'Completed'
        db.session.commit()
        flash("Order closed successfully", "success")   
    else:
        flash("Order is not in a state to be completed", "danger")

    # Redirect to the orders page after completing the order    
    return redirect(url_for('admin.orders'))


@admin.route("/completed_orders")
@admin_required
def completedOrders():
    completedOrders = Order.query.filter_by(order_status='Completed').all()  # Assuming 'Completed' means archived orders
    return render_template("admin/older_orders.html", archived_orders=completedOrders)


@admin.route("/add_product", methods=["GET", "POST"])
# @admin_required
def addProduct():
    form = ProductForm()

    if form.validate_on_submit():
        if not form.image.data:
            flash("Please upload at least one product image.", "danger")
            return render_template("admin/add_product.html", form=form)
        print(form.image.data)
        print('Form submitted successfully')
        print("Form data:", form.data)
        image_name = upload_img(form.image.data)
        p=Product(name=form.name.data, description=form.description.data, price=form.price.data, sizes=','.join(form.sizes.data), image=image_name, num_images=len(form.image.data))
        db.session.add(p)
        db.session.commit()  # Assuming this function handles the image upload
        return redirect(url_for('admin.allProducts'))
        
        

    return render_template("admin/add_product.html", form=form)



@admin.route("/all_products")
@admin_required
def allProducts():
    products = Product.query.order_by(Product.is_active.desc()).all()  # Fetch all products from the database
    return render_template("admin/products.html", products=products)


@admin.route("/restock_product")
@admin_required
def restockProduct():
    p = request.args.get('p')
    product = Product.query.filter_by(id=p).first()
    if product:
        if not product.is_active:
            product.is_active = True  # Mark the product as inactive
            db.session.commit()
            flash("Product Restock successfully", "success")
        else:
            flash("Product is already active", "info")       
    else:
        flash("Product not found", "danger")    
    return redirect(url_for('admin.allProducts'))

@admin.route("/remove_product")
@admin_required
def removeProduct():
    p = request.args.get('p')
    product = Product.query.filter_by(id=p).first()
    if product:
        if product.is_active:
            product.is_active = False  # Mark the product as inactive
            db.session.commit()
            flash("Product removed successfully", "success")       
        else:
            flash("Product is already inactive", "warning")
    else:
        flash("Product not found", "danger")    
    return redirect(url_for('admin.allProducts'))


@admin.route("/edit_product")
@admin_required
def editProduct():
    p = request.args.get('p')
    product = Product.query.filter_by(id=p).first()
    if product:
        product.is_active = False  # Mark the product as inactive
        db.session.commit()
        flash("Product removed successfully", "success")       
    else:
        flash("Product not found", "danger")    
    return redirect(url_for('admin.allProducts'))



@admin.route("/login", methods=["GET", "POST"])
def index():

    session.clear()
    return redirect(login)


@admin.route("/otp", methods=["POST"])
def otp():

    if not request.form.get('otp'):

        return jsonify(
                {
                    "status" : "error",
                    "message" : "Otp Missing"
                })

    elif not session.get("otp") == request.form.get('otp'):

        session['otp'] = generateOTP()
        return jsonify(
                {
                    "status" : "error",
                    "message" : "Invalid Otp!"
                })

    else:
        session.clear()
        session['admin'] = True
        return jsonify(
                {
                    "status" : "success",
                    "message" : "Otp Matched"
                })

""" remove a product """
@admin.route("/removeProduct")
def remove_product():

    if True: # session.get('admin')

        p = request.args.get('p')

        # do the database deletion
        with db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("DELETE FROM products WHERE (product_id=(%s))", (p,))

        remove_img(productId=p)
        return jsonify(True)
    else:
        return "Method Not allowed"




""" adding a new product """
@admin.route("/add_product", methods=["POST"])
@admin_required
def add_product():

    if True: # session.get('admin')

        if 'file' not in request.files:
            flash(u"No file part", "danger")
            return redirect(request.url)

        prodname = request.form.get("product")
        price = request.form.get("price")
        proddesc = request.form.get("productdesc")

        sizes = request.form.getlist("size")  # taking all the sizes input by the user via form.getlist
        sizes_available = ""
        for size in sizes:
            sizes_available = sizes_available + ", " + size
        sizes_available = sizes_available.lstrip(', ')

        files = request.files.getlist("file")

        with db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(f"INSERT INTO products (product_name, product_desc, price, sizes_available) VALUES ({prodname}, {proddesc}, {price}, {sizes_available})", (prodname, proddesc, price, sizes_available,))
                product_id

        upload_img(files, product_id)

        return redirect('/admin/dashboard')

    return redirect("/admin")



""" admin loggin out """
@admin.route("/logout")
@admin_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/admin")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("InternalServerError.html", error=e.name, code = e.code)


# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)