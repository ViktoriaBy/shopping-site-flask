"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
import customers



import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                    melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                    display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    order_total = 0
    
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    melons_in_cart = []
    
    # - get the cart dictionary from the session
    cart = session.get("cart", {})
    
    
    # - loop over the cart dictionary, and for each melon id:
    for melon_id, quantity in cart.items():
        
    #    - get the corresponding Melon object
        melon = melons.get_by_id(melon_id)
    #    - compute the total cost for that type of melon
    #    - add this to the order total
        total_cost = melon.price * quantity
        order_total += total_cost 
        
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
        melon.quantity = quantity
        melon.total_cost = total_cost
    
    
        melons_in_cart.append(melon)
    # - pass the total order cost and the list of Melon objects to the template
    return render_template("cart.html", cart=melons_in_cart, order_total=order_total)
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # Check if we have a cart in the session and if not, add one
    # Also, bind the cart to the name 'cart' for easy reference below
    if 'cart' in session:
        cart = session['cart']
    else:
        cart = session['cart'] = {}

    # We could also do this with setdefault:
    # cart = session.setdefault("cart", {})

    # Add melon to cart - either increment the count (if melon already in cart)
    # or add to cart with a count of 1
    cart[melon_id] = cart.get(melon_id, 0) + 1

    # Print cart to the terminal for testing purposes
    # print("cart:")
    # print(cart)

    # Show user success message on next page load
    flash("Melon successfully added to cart.")

    # Redirect to shopping cart page
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    user = customers.get_by_email(email)

    if not user:
        flash("No such email address.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    session["logged_in_customer_email"] = user.email
    flash("Logged in.")
    return redirect("/melons")


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_customer_email"]
    flash("Logged out.")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
