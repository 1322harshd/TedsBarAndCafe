from flask import Flask, render_template,request
from models import db, Product, Size, ProductPrice, CartItem, PaymentInfo
import uuid
from collections import defaultdict
from flask import Flask, render_template, request, session, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# Database configuration (SQLite for example)
# change URI to PostgreSQL/MySQL if required
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2003@localhost:5432/TedsBarAndCafeDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database and migration
migrate = Migrate(app, db)  # <-- This line is required!

# initialize db with app
db.init_app(app)


# helper function → groups products by category
def group_items(item_list):
    grouped = defaultdict(list)
    for item in item_list:
        grouped[item.category.strip()].append(item)
    return grouped


# route → shows the full menu grouped by categories
@app.route("/menu")
def menu_page():
    items = Product.query.all()  # fetch all products
    grouped_items = group_items(items)  # group by category
    return render_template("menu_page.html", grouped_items=grouped_items)


# route → shows products filtered by category (like "Hot Coffees")
@app.route("/filter/<category>")
def filter_category(category):
    filtered = Product.query.filter(Product.category.ilike(category)).all()
    grouped_items = group_items(filtered)
    return render_template("category.html", grouped_items=grouped_items)


# route → shows details of a single product, including sizes and prices
@app.route("/product/<int:id>")
def selected_product(id):
    # Get the product the user clicked on
    product = Product.query.get_or_404(id)

    # Get related products (same category, but not the same product)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()  # limit to 4 items for display

    return render_template("selected_product_page.html", product=product, related_products=related_products)

 
# Contact page route
@app.route('/contact')
def contact():
    # Render the contact us page template
    return render_template('Contact_uspage.html')

# Cart page route
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_img = request.form.get('product_img')
        size = request.form.get('size')
        size_price_map = {'small': 5.0, 'medium': 7.0, 'large': 9.0}
        price = size_price_map.get(size, 5.0)
        cart_item = {
            'id': product_id,
            'name': product_name,
            'image': product_img,
            'size': size,
            'price': price,
            'quantity': 1
        }
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(cart_item)
        session.modified = True

        
        if 'sid' not in session:
            session['sid'] = str(uuid.uuid4())

        new_cart_item = CartItem(
            session_id=session['sid'],
            product_id=product_id,
            product_name=product_name,
            product_img=product_img,
            size=size,
            price=price,
            quantity=1
        )
        db.session.add(new_cart_item)
        db.session.commit()

        # After adding, redirect to GET so the cart page updates
        return redirect(url_for('cart'))

    # For GET, show the cart
    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    total_quantity = sum(item['quantity'] for item in cart_items)
    if total_quantity >= 5:
        other_charges = round(subtotal * 0.015, 2)
    else:
        other_charges = 0.00
    taxes = round(subtotal * 0.18, 2)
    total = round(subtotal + taxes + other_charges, 2)
    return render_template(
        'Shopping_cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        taxes=taxes,
        other_charges=other_charges,
        total=total
    )

# Payment page route
@app.route('/Payment')
def payment():
    # Get summary values from query parameters
    subtotal = request.args.get('subtotal', 0, type=float)
    taxes = request.args.get('taxes', 0, type=float)
    other_charges = request.args.get('other_charges', 0, type=float)
    total = request.args.get('total', 0, type=float)
    # Render the payment page with summary values
    return render_template(
        'payment.html',
        subtotal=subtotal,
        taxes=taxes,
        other_charges=other_charges,
        total=total
    )

# Feedback page route
@app.route('/feedback')
def feedback():
    # Placeholder for feedback page
    return "<h2>Feedback page coming soon!</h2>"

# Remove item from cart route
@app.route('/remove_from_cart/<int:index>', methods=['POST'])
def remove_from_cart(index):
    if 'cart' in session and 0 <= index < len(session['cart']):
        session['cart'].pop(index)
        session.modified = True
    return redirect(url_for('cart'))


# Order confirmation and payment validation route
@app.route('/order_confirmation', methods=['GET', 'POST'])
def order_confirmation():
    if request.method == 'POST':
        # Get form data from payment page
        fullname = request.form.get('fullname', '').strip()
        card_number = request.form.get('card_number', '').replace(' ', '').replace('-', '')
        expiry = request.form.get('expiry', '').strip()
        cvc = request.form.get('cvc', '').strip()
        card_name = request.form.get('card_name', '').strip()
        errors = []

        # Get summary values from hidden fields
        subtotal = request.form.get('subtotal', 0, type=float)
        taxes = request.form.get('taxes', 0, type=float)
        other_charges = request.form.get('other_charges', 0, type=float)
        total = request.form.get('total', 0, type=float)

        # Validate payment details
        if not fullname:
            errors.append("Full name is required.")
        if not card_number.isdigit() or len(card_number) != 16:
            errors.append("Card number must be exactly 16 digits.")
        import re, datetime
        exp_match = re.match(r'^(\d{2})/(\d{2})$', expiry)
        if not exp_match:
            errors.append("Expiry must be in MM/YY format.")
        else:
            mm, yy = int(exp_match.group(1)), int(exp_match.group(2)) + 2000
            now = datetime.datetime.now()
            exp_date = datetime.datetime(yy, mm, 1)
            if mm < 1 or mm > 12 or exp_date < now.replace(day=1):
                errors.append("Card expired or invalid month.")
        if not (cvc.isdigit() and len(cvc) == 3):
            errors.append("CVC must be exactly 3 digits.")
        if not card_name:
            errors.append("Name on card is required.")

        # If there are errors, re-render payment page with errors
        if errors:
            # Payment failed, show payment form again
            return render_template(
                'payment.html',
                errors=errors,
                subtotal=subtotal,
                taxes=taxes,
                other_charges=other_charges,
                total=total
            )
        
        if 'sid' not in session:
            session['sid'] = str(uuid.uuid4())

        payment_info = PaymentInfo(
            session_id=session['sid'],
            fullname=fullname,
            email=request.form.get('email', ''),
            phone=request.form.get('phone', ''),
            address=request.form.get('address', ''),
            instructions=request.form.get('instructions', ''),
            card_number=card_number,
            expiry=expiry,
            cvc=cvc,
            card_name=card_name,
            subtotal=subtotal,
            taxes=taxes,
            other_charges=other_charges,
            total=total
        )
        db.session.add(payment_info)
        db.session.commit()

        # if the Payment successful, show confirmation with success=True
        return render_template('order_confirmation.html', success=True)
    # If GET request, show confirmation with success=False optional
    return render_template('order_confirmation.html', success=False)

# Run the development server
if __name__ == '__main__':
    app.run(debug=True)