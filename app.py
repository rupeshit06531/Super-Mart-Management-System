"""
Import all required modules for the Super Mart Management System.

These modules are used to create the Flask application,
manage user requests, connect to the database,
and work with database models.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from database import db

# Used to generate a secure file name
from werkzeug.utils import secure_filename

# Used to work with folders and file paths
import os

# Import the required database models.
from models import (
    Admin,
    Product,
    Customer,
    Invoice
)


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

# Create upload folder if it does not exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


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
    """

    # Check whether the administrator is logged in
    if "admin_id" not in session:

        # Show warning message
        flash("Please login first.", "warning")

        # Redirect to login page
        return redirect(url_for("login"))

    # Count total products
    total_products = Product.query.count()

    # Count total customers
    total_customers = Customer.query.count()

    # Count total invoices
    total_invoices = Invoice.query.count()

    # Get latest 5 invoices
    recent_invoices = Invoice.query.order_by(
        Invoice.created_at.desc()
    ).limit(5).all()

    # Calculate total stock of all products
    total_stock = db.session.query(
        db.func.sum(Product.stock)
    ).scalar() or 0

    # Count products with stock less than or equal to 5
    low_stock = Product.query.filter(
        Product.stock <= 5
    ).count()

    # Get the latest 5 products
    recent_products = Product.query.order_by(
        Product.id.desc()
    ).limit(5).all()

    # Open dashboard page
    return render_template(
    "dashboard.html",
    total_products=total_products,
    total_customers=total_customers,
    total_stock=total_stock,
    low_stock=low_stock,
    recent_products=recent_products,
    total_invoices=total_invoices,
    recent_invoices=recent_invoices
    
    )


@app.route("/logout")
def logout():
    """
    Logout the administrator.
    """

    # Remove all session data
    session.clear()

    # Show success message
    flash("Logout successful.", "success")

    # Redirect to login page
    return redirect(url_for("login"))


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

        # Read uploaded image
        image = request.files.get("image")

        # Default image name
        image_name = None

        # Check whether an image is uploaded
        if image and image.filename != "":

            # Generate a secure file name
            image_name = secure_filename(image.filename)

            # Save image into upload folder
            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    image_name
                )
            )

        # Create a new product object
        new_product = Product(

            # Store product name
            name=name,

            # Store product category
            category=category,

            # Store product price
            price=price,

            # Store available stock
            stock=stock,

            # Store uploaded image name
            image=image_name
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
    Display the Edit Product page and update product information.
    """

    # Check whether the administrator is logged in
    if "admin_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Retrieve the selected product
    product = Product.query.get_or_404(id)

    # Check whether the form has been submitted
    if request.method == "POST":

        # Read updated values from the form
        name = request.form.get("name").strip()
        category = request.form.get("category").strip()
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock"))

        # Check whether another product already has the same name
        existing_product = Product.query.filter(
            Product.name == name,
            Product.id != product.id
        ).first()

        if existing_product:
            flash("Product name already exists.", "danger")
            return render_template("edit_product.html", product=product)

        # Validate product price
        if price <= 0:
            flash("Price must be greater than zero.", "danger")
            return render_template("edit_product.html", product=product)

        # Validate product stock
        if stock < 0:
            flash("Stock cannot be negative.", "danger")
            return render_template("edit_product.html", product=product)

        # Update product information
        product.name = name
        product.category = category
        product.price = price
        product.stock = stock

        # Save changes into the database
        db.session.commit()

        # Display success message
        flash("Product updated successfully.", "success")

        # Redirect to product list page
        return redirect(url_for("products"))

    # Display Edit Product page
    return render_template("edit_product.html", product=product)


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

    # Delete product image if it exists
    if product.image:

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            product.image
        )

        # Check whether the image file exists
        if os.path.exists(image_path):

            # Delete the image file
            os.remove(image_path)

    # Delete the selected product from the database
    db.session.delete(product)

    # Save changes into the database
    db.session.commit()

    # Save the changes into the database.
    db.session.commit()

    # Display a success message.
    flash("Product deleted successfully.", "success")

    # Redirect to the Products page.
    return redirect(url_for("products"))

@app.route("/products")
def products():
    """
    Display all products with search functionality.
    """

    # Check whether the administrator is logged in
    if "admin_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Read search keyword from URL
    search = request.args.get("search", "").strip()

    # Check whether the user entered a search keyword
    if search:

        # Search products by name or category
        product_list = Product.query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.category.ilike(f"%{search}%"))
        ).order_by(Product.id.desc()).all()

    else:

        # Retrieve all products
        product_list = Product.query.order_by(Product.id.desc()).all()

    # Count total products
    total_products = len(product_list)

    # Display the Products page
    return render_template(
        "products.html",
        products=product_list,
        total_products=total_products,
        search=search
    )

@app.route("/product/<int:id>")
def product_details(id):
    """
    Display product details.
    """

    # Check whether the administrator is logged in
    if "admin_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Get product by id
    product = Product.query.get_or_404(id)

    # Open product details page
    return render_template(
        "product_details.html",
        product=product
    )

@app.route("/billing")
def billing():

    @app.route("/save-invoice", methods=["POST"])
    def save_invoice():
        """
        Save invoice into the database.
        """

        # Read data from form
        bill_number = request.form.get("bill_number")
        customer_name = request.form.get("customer_name")
        total_amount = request.form.get("total_amount")

        # Create invoice object
        invoice = Invoice(
            bill_number=bill_number,
            customer_name=customer_name,
            total_amount=float(total_amount)
        )

        # Save invoice
        db.session.add(invoice)
        db.session.commit()

        flash("Invoice saved successfully.", "success")

        return redirect(url_for("billing"))
    
    @app.route("/invoice-history")
    def invoice_history():
        """
        Display all saved invoices.
        """

        # Check whether admin is logged in
        if "admin_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        # Read search value
        search = request.args.get("search", "").strip()

        # Check whether search is entered
        if search:

            invoices = Invoice.query.filter(
                Invoice.bill_number.ilike(f"%{search}%")
            ).order_by(
                Invoice.created_at.desc()
            ).all()

        else:

            invoices = Invoice.query.order_by(
                Invoice.created_at.desc()
            ).all()
            

        # Open invoice history page
        return render_template(
            "invoice_history.html",
            invoices=invoices,
            search=search
        )
    
    @app.route("/delete-invoice/<int:id>")
    def delete_invoice(id):
        """
        Delete selected invoice.
        """

        # Check whether admin is logged in
        if "admin_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        # Get invoice by id
        invoice = Invoice.query.get_or_404(id)

        # Delete invoice
        db.session.delete(invoice)

        # Save changes
        db.session.commit()

        flash("Invoice deleted successfully.", "success")

        return redirect(url_for("invoice_history"))
    
    @app.route("/invoice/<int:id>")
    def view_invoice(id):
        """
        Display invoice details.
        """

        # Check whether admin is logged in
        if "admin_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        # Get invoice by ID
        invoice = Invoice.query.get_or_404(id)

        # Open invoice details page
        return render_template(
            "view_invoice.html",
            invoice=invoice
        )
    
    @app.route("/invoice/pdf/<int:id>")
    def invoice_pdf(id):
        """
        Download invoice as PDF.
        """

        # Check whether admin is logged in
        if "admin_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        # Get invoice
        invoice = Invoice.query.get_or_404(id)

        return render_template(
            "invoice_pdf.html",
            invoice=invoice
        )
    
    @app.route("/sales-report")
    def sales_report():
        """
        Display Sales Report page.
        """

        # Check whether admin is logged in
        if "admin_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        # Get all invoices
        invoices = Invoice.query.order_by(
            Invoice.created_at.desc()
        ).all()

        # Calculate total sales
        total_sales = sum(
            invoice.total_amount
            for invoice in invoices
        )

        # Total invoices
        total_invoices = len(invoices)

        # Calculate today's sales
        today_sales = sum(
            invoice.total_amount
            for invoice in invoices
            if invoice.created_at.date() == datetime.today().date()
        )

        # Calculate this month's sales
        current_month = datetime.today().month
        current_year = datetime.today().year

        month_sales = sum(
            invoice.total_amount
            for invoice in invoices
            if invoice.created_at.month == current_month
            and invoice.created_at.year == current_year
        )

        # Calculate this year's sales
        year_sales = sum(
            invoice.total_amount
            for invoice in invoices
            if invoice.created_at.year == current_year
        )


        # Open Sales Report page
        return render_template(
        "sales_report.html",
        invoices=invoices,
        total_sales=total_sales,
        total_invoices=total_invoices,
        today_sales=today_sales,
        month_sales=month_sales,
        year_sales=year_sales
    )

    @app.route("/export-sales")
    def export_sales():
        """
        Export sales report as CSV.
        """

        # Check login
        if "admin_id" not in session:
            return redirect(url_for("login"))

        # Get all invoices
        invoices = Invoice.query.all()

        # CSV header
        csv_data = "Bill No,Customer,Total,Date\n"

        # Add invoice data
        for invoice in invoices:

            csv_data += (
                f"{invoice.bill_number},"
                f"{invoice.customer_name},"
                f"{invoice.total_amount},"
                f"{invoice.created_at}\n"
            )

        # Return CSV file
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=sales_report.csv"
            }
        )


    """
    Display the Billing page.
    """

    # Check whether the administrator is logged in
    if "admin_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Get all products
    products = Product.query.order_by(Product.name).all()

    # Open Billing page
    return render_template(
        "billing.html",
        products=products
    )



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

@app.errorhandler(404)
def page_not_found(error):
    """
    Display custom 404 page.
    """

    return render_template("404.html"), 404


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