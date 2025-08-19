from fitkit import db, bcrypt
from app import app

from fitkit.product.models import Product
from fitkit.users.models import Cart, User, Order
from werkzeug.security import generate_password_hash


with app.app_context():
    db.create_all()

    hashed_password = bcrypt.generate_password_hash('raj').decode('utf-8')
    u = User(username='Raj', email='raj@gmail.com', password=hashed_password)

    hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    a = User(username='Admin', email='admin@gmail.com', password=hashed_password, role='admin')
    # c = Cart(quantity=10, size='s', product=p, cart_user=u)
    # o = Order(address= 'Raj' \
    # '9874801938'\
    # '1 Rani RashMoni Road, Dakshineswar Kolkata West Bengal-700035', 
    #     order_size=c.size, order_quantity=c.quantity, product=c.product, order_user=u)
    db.session.add(a)
    db.session.add(u)
    db.session.commit()