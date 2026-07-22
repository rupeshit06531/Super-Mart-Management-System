import os
from flask import Flask, render_template, request
from database import db
from models import Admin

app = Flask(__name__)



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database", "supermart.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True)