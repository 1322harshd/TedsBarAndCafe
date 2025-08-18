from flask import Flask,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:13Dhillon%40nz@localhost:5432/TedsBarAndCafeDatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)   # initialize here
migrate = Migrate(app, db)

from models import Product, Size, ProductPrice  # import after db is created

#about page route
@app.route("/about")
def about_page():
  return render_template('about_page.html')
#menu route with all item display functionality
items = [
    {'id':1,'name': 'Espresso', 'category': 'hot-coffees','img':'cappucino.png','price':'$5'},
    {'id':2,'name': 'Latte', 'category': 'hot-coffees','img':'cappucino.png','price':'$5'},
    {'id':3,'name': 'Green Tea', 'category': 'Tea','img':'cappucino.png','price':'$5'},
    {'id':4,'name': 'Black Tea', 'category': 'Tea','img':'cappucino.png','price':'$5'},
    {'id':5,'name': 'Croissant', 'category': 'Pastry','img':'cappucino.png','price':'$5'}
]

@app.route("/menu")
def menu_page():
    grouped_items = group_items(items)  # All items
    return render_template("menu_page.html", grouped_items=grouped_items)

@app.route("/filter/<category>")
def filter_category(category):
    filtered = [item for item in items if item['category'].lower() == category.lower()]
    grouped_items = group_items(filtered)
    return render_template("category.html", grouped_items=grouped_items)

def group_items(item_list):
    grouped = defaultdict(list)
    for item in item_list:
        grouped[item['category']].append(item)
    return grouped

# hardcoded selected product page
@app.route("/spp/<int:id>")
def selected_product(id):
       # find the product with matching id
    product = next((p for p in items if p["id"] == id), None)
    if not product:
        return "Product not found", 404

    # find related products from same category
    related = [p for p in items if p["category"] == product["category"] and p["id"] != id]

    return render_template("selected_product_page.html", product=product, related=related)



@app.route('/contact')
def contact():
    return render_template('Contact_uspage.html')
@app.route('/cart')
def cart():
    # example cart items
    cart_items = [
        {'id': 1, 'name': 'Cappuccino', 'image': 'cappuccino.png', 'quantity': 2, 'price': 4.50},
        {'id': 2, 'name': 'Sandwich', 'image': 'sandwich.png', 'quantity': 1, 'price': 6.00}
    ]
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    taxes = round(subtotal * 0.10, 2)  # Example 10% tax
    other_charges = 2.00  # Example other charges
    total = round(subtotal + taxes + other_charges, 2)
    return render_template(
        'Shopping_cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        taxes=taxes,
        other_charges=other_charges,
        total=total
    )
@app.route('/payment')
def payment():
    return render_template('payment.html')
@app.route('/feedback')
def feedback():
    return "<h2>Feedback page coming soon!</h2>"
@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

# Run the development server
if __name__ == '__main__':
    app.run(debug=True)