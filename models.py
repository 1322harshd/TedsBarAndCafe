
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

# model for products

# ...existing code...
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)      
    image_url = db.Column(db.String(300), nullable=True)
    def __repr__(self):
        return f"<Product {self.name}>"

class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False) 

class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product', backref='prices')
    size = db.relationship('Size')

    def __repr__(self):
        return f"<{self.product.name} - {self.size.name}: {self.price}>"

# New model for cart items
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    product_img = db.Column(db.String(300), nullable=True)
    size = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

# New model for payment info
class PaymentInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    card_number = db.Column(db.String(20), nullable=False)
    expiry = db.Column(db.String(10), nullable=False)
    cvc = db.Column(db.String(5), nullable=False)
    card_name = db.Column(db.String(100), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    taxes = db.Column(db.Float, nullable=False)
    other_charges = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
