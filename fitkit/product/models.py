from datetime import datetime
from fitkit import db
from fitkit.users.models import Cart, Order

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(225), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    sizes = db.Column(db.String(), nullable=False) # it will be a string of s,m,l,xl,xxl
    # quantity = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    image = db.Column(db.String(20), nullable=False)
    num_images = db.Column(db.Integer, nullable=False, default=1)  # Number of images uploaded
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

    cart = db.relationship('Cart', back_populates='product', lazy=True)
    order = db.relationship('Order', back_populates='product', lazy=True)

    

    def __repr__(self):
        return f"product('{self.id}, {self.name}, {self.description}, {self.image})"
    

