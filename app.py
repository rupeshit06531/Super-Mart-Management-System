import os
from flask import Flask, render_template, request, redirect
from database import db
from models import Admin, Product

app = Flask(__name__)



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database", "supermart.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:
            return render_template("dashboard.html")

        return "Invalid Username or Password"

    return render_template("login.html")


with app.app_context():
    db.create_all()

    admin = Admin.query.filter_by(username="admin").first()

    if not admin:
        admin = Admin(
            username="admin",
            password="admin123"
        )

        db.session.add(admin)
        db.session.commit()


@app.route("/products")
def products():
    all_products = Product.query.all()
    return render_template(
        "products/product_list.html",
        products=all_products
    )

@app.route("/products/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product = Product(
            name=request.form["name"],
            category=request.form["category"],
            price=float(request.form["price"]),
            stock=int(request.form["stock"])
        )

        db.session.add(product)
        db.session.commit()

        return redirect("/products")

    return render_template("products/add_product.html")


@app.route("/products/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])

        db.session.commit()

        return redirect("/products")

    return render_template(
        "products/edit_product.html",
        product=product
    )

@app.route("/products/delete/<int:id>")
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/products")


if __name__ == "__main__":
    app.run(debug=True)