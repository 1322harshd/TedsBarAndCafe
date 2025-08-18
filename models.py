from app import db

# model for products
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
    name = db.Column(db.String(20), nullable=False)  # Small, Medi

class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product', backref='prices')
    size = db.relationship('Size')

    def __repr__(self):
        return f"<{self.product.name} - {self.size.name}: {self.price}>"
