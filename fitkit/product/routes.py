from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from fitkit import db
from fitkit.product.models import Product

product = Blueprint('product', __name__,
                        template_folder='templates', static_folder='static', static_url_path='/product/static')

""" index page """
@product.route("/")
@product.route("/<int:page>/")
def index(page=1):

    sort_by = request.args.get('sort_by', 'newer', type=str)
    print(sort_by, page)
    '''
    sort_by values will be:
    1. newer <default> - creation_date desc
    2. older - creation_date asc
    3. low_to_high - low price first
    4. high_to_low - high price first
    '''

    if sort_by == 'newer':
        items = Product.query.order_by(Product.creation_date.desc()).paginate(page=page, per_page=5)
    elif sort_by == 'older':
        items = Product.query.order_by(Product.creation_date).paginate(page=page, per_page=5)
    elif sort_by == 'low_to_high':
        items = Product.query.order_by(Product.price).paginate(page=page, per_page=5)
    elif sort_by == 'high_to_low':
        items = Product.query.order_by(Product.price.desc()).paginate(page=page, per_page=5)
    else:
        abort(403)

    print(dir(items))
    print(items.items)
    print(items.items[0].id)

    # return '<h1>Hello, world</h1>'
    return render_template("product/index.html", items=items, sort=sort_by)


""" single product detail """
@product.route("/detail/<int:product_id>/")
def detail(product_id=1):

    print(product_id)
    product = Product.query.get_or_404(product_id)

    related_products = Product.query.filter(Product.id != product.id).limit(4)

    print(11111, product.sizes)
    sizes = product.sizes.split(',')
    print(related_products)
    print(111, sizes)

    # single_product[0]["sizes_available"] = single_product[0]["sizes_available"].replace(' ', '').split(',')
    # print(single_product)

    return render_template("product/productDetail.html", product=product, sizes=sizes, related_products=related_products)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("InternalServerError.html", error=e.name, code = e.code)


# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)