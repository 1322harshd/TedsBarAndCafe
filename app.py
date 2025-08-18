from flask import Flask,render_template
from collections import defaultdict
from flask import Flask, render_template, request

app = Flask(__name__)

# About page route
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


    # Render the about page template
    return render_template('about_page.html')

# Contact page route
@app.route('/contact')
def contact():
    # Render the contact us page template
    return render_template('Contact_uspage.html')

# Cart page route
@app.route('/cart')
def cart():
    # example cart items
    # Example cart items (would be dynamic in a real app)
    cart_items = [
       
    ]
    # Calculate subtotal
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    # Calculate total quantity
    total_quantity = sum(item['quantity'] for item in cart_items)
    # Apply other charges only if 3 or more items are ordered
    if total_quantity >= 3:
        other_charges = round(subtotal * 0.015, 2)  # 1.5% of subtotal
    else:
        other_charges = 0.00
    taxes = round(subtotal * 0.18, 2)  # 18% tax
    total = round(subtotal + taxes + other_charges, 2)
    # Render the shopping cart template with calculated values
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
        # if the Payment successful, show confirmation with success=True
        return render_template('order_confirmation.html', success=True)
    # If GET request, show confirmation with success=False optional
    return render_template('order_confirmation.html', success=False)

# Run the development server
if __name__ == '__main__':
    app.run(debug=True)