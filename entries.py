from fitkit import db
from app import app

from fitkit.product.models import Product
from fitkit.users.models import Cart, User, Order


with app.app_context():
    db.create_all()


    # u = User(username='Raj', email='raj@gmail.com', password='123')
    # a = User(username='Admin', email='admin@gmail.com', password='admin123', role='admin')
    # # c = Cart(quantity=10, size='s', product=p, cart_user=u)
    # # o = Order(address= 'Raj' \
    # # '9874801938'\
    # # '1 Rani RashMoni Road, Dakshineswar Kolkata West Bengal-700035', 
    # #     order_size=c.size, order_quantity=c.quantity, product=c.product, order_user=u)
    # db.session.add(a)
    # db.session.add(u)
    # db.session.commit()