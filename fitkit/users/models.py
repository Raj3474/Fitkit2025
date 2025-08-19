from datetime import datetime
from fitkit import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user') # two types - admin, user

    cart = db.relationship('Cart', back_populates='cart_user', lazy=True)
    order = db.relationship('Order', back_populates='order_user', lazy=True)
    


    def __repr__(self):
        return f"User('{self.username}', '{self.email}'')"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(20), nullable=False)

    # defining relationship between, Product and Cart
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='cart', lazy=True)
    

    # defining relationship between, User and Cart
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cart_user = db.relationship('User', back_populates='cart', lazy=True)



    def __repr__(self):
        return f"Post({self.quantity}, {self.size}, {self.product.name})"
    

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(225), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now())
    order_status = db.Column(db.String(20), nullable=False, default='Booked')
    order_quantity = db.Column(db.Integer, nullable=False)
    order_size = db.Column(db.String(20), nullable=False)


    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='order', lazy=True)

    '''
    creating the relationship between user and order tables.
    '''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_user = db.relationship('User', back_populates='order', lazy=True)


    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.image_file}')"