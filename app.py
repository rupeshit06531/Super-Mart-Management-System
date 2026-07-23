"""
Import all required modules for the Super Mart Management System.

These modules are used to create the Flask application,
manage user requests, connect to the database,
and work with database models.
"""

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from database import db

# Import the required database models.
from models import Admin, Product, Customer


# ==========================================================
# Create Flask Application
# This object manages the entire web application.
# ==========================================================

app = Flask(__name__)


# ==========================================================
# Flask Application Configuration
# This section configures the application settings
# such as the database, session security, and file paths.
# ==========================================================

# Configure the SQLite database used by the application.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///supermart.db"

# Disable unnecessary modification tracking to improve performance.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set the secret key used to secure user sessions and flash messages.
app.config["SECRET_KEY"] = "supermart_secret_key_2026"

# Configure the folder used to store uploaded product images.
# This folder will be created later in the project.
app.config["UPLOAD_FOLDER"] = "static/uploads"


# ==========================================================
# Configure Application
# These settings define how the application connects
# to the SQLite database.
# ==========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///supermart.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supermart_secret_key"


# ==========================================================
# Initialize the Database
# This section connects SQLAlchemy with the Flask application
# so that all models can communicate with the database.
# ==========================================================

db.init_app(app)

# ==========================================================
# Create Database Tables
# This section creates all database tables when the
# application starts for the first time.
# ==========================================================

with app.app_context():

    # Create every table defined inside the models module.
    # If a table already exists, Flask will not recreate it.
    db.create_all()


# ==========================================================
# Create Default Administrator
# This section checks whether an administrator account
# already exists. If not, a default administrator account
# is created automatically.
# ==========================================================

with app.app_context():

    # Check whether the default administrator already exists.
    admin = Admin.query.filter_by(username="admin").first()

    if admin is None:

        # Create the default administrator account.
        default_admin = Admin(
            username="admin",
            password="admin123"
        )

        # Save the administrator account into the database.
        db.session.add(default_admin)
        db.session.commit()


# ==========================================================
# Create Database Tables
# This section automatically creates all database tables
# when they do not already exist.
# ==========================================================

with app.app_context():

    # Create every table defined inside the models module.
    # Existing tables will not be recreated.
    db.create_all()


# ==========================================================
# Application Startup Completed
# The application is now connected to the database
# and ready to process incoming requests.
# ==========================================================

# ==========================================================
# Login Module
# This module authenticates the administrator and
# grants access to the system.
# ==========================================================

# ==========================================================
# Home Route
# This route is the default entry point of the application.
# It displays a welcome message and confirms that the
# application is running successfully.
# ==========================================================

@app.route("/")
def home():
    """
    Display the home page.

    This function handles the default URL of the application.
    It is mainly used to verify that the Flask application
    is running correctly before adding more features.
    """

    # Return a simple welcome message to verify the application.
    return "<h2>Welcome to Super Mart Management System</h2>"


# ==========================================================
# Login Route
# This route displays the login page and verifies the
# administrator's login credentials.
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle administrator login.

    This function displays the login page when the user
    visits the page. It also validates the submitted
    username and password against the database.
    """

    # Check whether the login form has been submitted.
    if request.method == "POST":

        # Read the username entered by the administrator.
        username = request.form.get("username")

        # Read the password entered by the administrator.
        password = request.form.get("password")

        # Search for a matching administrator account.
        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        # Check whether the login credentials are valid.
        if admin:

            # Store the administrator information in the session.
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username

            # Display a success message.
            flash("Login successful.", "success")

            # Redirect the administrator to the dashboard.
            return redirect(url_for("dashboard"))

        # Display an error message if the login fails.
        flash("Invalid username or password.", "danger")

    # Display the login page.
    return render_template("login.html")

# ==========================================================
# Dashboard Module
# This module displays the main dashboard after
# successful administrator login.
# ==========================================================


# ==========================================================
# Dashboard Route
# This route displays the administrator dashboard
# after a successful login.
# ==========================================================

@app.route("/dashboard")
def dashboard():
    """
    Display the administrator dashboard.

    This function checks whether the administrator
    is logged in before allowing access to the dashboard.
    """

    # Check whether the administrator is logged in.
    if "admin_id" not in session:

        # Display an error message for unauthorized access.
        flash("Please login first.", "warning")

        # Redirect the user to the login page.
        return redirect(url_for("login"))

# Display the professional dashboard page.
# The dashboard interface is loaded from the HTML template.
        return render_template("dashboard.html")
    

# ==========================================================
# Product Management Module
# This module manages product operations including
# listing, adding, editing, and deleting products.
# ==========================================================



# ==========================================================
# Add Product Route
# This route displays the Add Product page and
# saves the new product into the database.
# ==========================================================

@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    """
    Display the Add Product page and save
    a new product into the database.
    """

    # Check whether the administrator is logged in.
    if "admin_id" not in session:

        # Redirect unauthorized users to the login page.
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Check whether the form has been submitted.
    if request.method == "POST":

        # Read the product information from the form.
        name = request.form.get("name")
        category = request.form.get("category")
        price = request.form.get("price")
        stock = request.form.get("stock")

        # ==========================================================
        # Validate the product information before saving.
        # This validation prevents duplicate products and
        # invalid values from being stored in the database.
        # ==========================================================

        # Remove extra spaces from the entered values.
        name = name.strip()
        category = category.strip()

        # Check whether the product name already exists.
        existing_product = Product.query.filter_by(name=name).first()

        if existing_product:

            # Display an error message.
            flash("Product name already exists.", "danger")

            # Reload the Add Product page.
            return render_template("add_product.html")

        # Convert values into numeric format.
        price = float(price)
        stock = int(stock)

        # Check whether the price is valid.
        if price <= 0:

            flash("Price must be greater than zero.", "danger")

            return render_template("add_product.html")

        # Check whether the stock quantity is valid.
        if stock < 0:

            flash("Stock cannot be negative.", "danger")

            return render_template("add_product.html")

        # Create a new product object.
        new_product = Product(

            name=name,

            category=category,

            price=price,

            stock=stock

        )

        # Save the product into the database.
        db.session.add(new_product)

        db.session.commit()

        # Display a success message.
        flash("Product added successfully.", "success")

        # Redirect to the Products page.
        return redirect(url_for("products"))

    # Display the Add Product page.
    return render_template("add_product.html")


# ==========================================================
# Edit Product Route
# This route displays the Edit Product page and
# updates the selected product information.
# ==========================================================

@app.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    """
    Display the Edit Product page and update
    the selected product information.
    """

    # Check whether the administrator is logged in.
    if "admin_id" not in session:

        # Redirect unauthorized users to the login page.
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Retrieve the selected product from the database.
    product = Product.query.get_or_404(id)

    # Check whether the form has been submitted.
    if request.method == "POST":

    # Check whether the form has been submitted.
        if request.method == "POST":

            # Read the updated product information.
            name = request.form.get("name").strip()
            category = request.form.get("category").strip()
            price = float(request.form.get("price"))
            stock = int(request.form.get("stock"))

            # Check whether another product already uses this name.
            existing_product = Product.query.filter(
                Product.name == name,
                Product.id != product.id
            ).first()

            if existing_product:

                # Display an error message.
                flash("Product name already exists.", "danger")

                # Reload the Edit Product page.
                return render_template(
                    "edit_product.html",
                    product=product
                )

            # Check whether the price is valid.
            if price <= 0:

                flash("Price must be greater than zero.", "danger")

                return render_template(
                    "edit_product.html",
                    product=product
                )

            # Check whether the stock is valid.
            if stock < 0:

                flash("Stock cannot be negative.", "danger")

                return render_template(
                    "edit_product.html",
                    product=product
                )

            # Update the product information.
            product.name = name
            product.category = category
            product.price = price
            product.stock = stock

            # Save the updated information into the database.
            db.session.commit()

            # Display a success message.
            flash("Product updated successfully.", "success")

            # Redirect to the Products page.
            return redirect(url_for("products"))


   

    # Check whether the stock is valid.
    if stock < 0:

        flash("Stock cannot be negative.", "danger")

        return render_template(
            "edit_product.html",
            product=product
        )

    # Update the product information.
    product.name = name
    product.category = category
    product.price = price
    product.stock = stock

    # Save the updated information into the database.
    db.session.commit()

    # Display a success message.
    flash("Product updated successfully.", "success")

    # Redirect to the Products page.
    return redirect(url_for("products"))


    # Display the Edit Product page.
    return render_template(
        "edit_product.html",
        product=product
    )


# ==========================================================
# Delete Product Route
# This route deletes the selected product from
# the database after validating the administrator.
# ==========================================================

@app.route("/delete-product/<int:id>")
def delete_product(id):
    """
    Delete the selected product from the database.
    """

    # Check whether the administrator is logged in.
    if "admin_id" not in session:

        # Redirect unauthorized users to the login page.
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Retrieve the selected product.
    product = Product.query.get_or_404(id)

    # Delete the selected product.
    db.session.delete(product)

    # Save the changes into the database.
    db.session.commit()

    # Display a success message.
    flash("Product deleted successfully.", "success")

    # Redirect to the Products page.
    return redirect(url_for("products"))

# ==========================================================
# Customer Management Module
# This module displays the customer list.
# ==========================================================

@app.route("/customers")
def customers():
    """
    Display all customers.
    """

    # Check whether the administrator is logged in.
    if "admin_id" not in session:

        # Redirect unauthorized users to the login page.
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Retrieve all customers from the database.
    customer_list = Customer.query.order_by(Customer.id.desc()).all()

    # Display the customer list page.
    return render_template(
        "customers.html",
        customers=customer_list
    )


# ==========================================================
# Run the Flask Application
# This section starts the Flask development server.
# The application will listen for incoming requests
# and display the website in your web browser.
# ==========================================================

if __name__ == "__main__":

    # Start the Flask development server.
    # Debug mode automatically reloads the application
    # whenever the source code is modified.
    app.run(debug=True)