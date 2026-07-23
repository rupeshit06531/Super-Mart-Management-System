"""
Super Mart Management System
----------------------------

Purpose:
This module defines all database models used in the application.
Each model represents a table in the database and stores
application data.

Author: Your Name
"""

from database import db


class Admin(db.Model):
    """
    Store administrator account information.

    This model is used to authenticate administrators
    who can access the Super Mart Management System.
    """

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """
        Return a readable representation of the administrator.
        """
        return f"<Admin {self.username}>"


class Product(db.Model):
    """
    Store product information.

    This model keeps all product details such as
    product name, category, price, and available stock.
    """

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        Return a readable representation of the product.
        """
        return f"<Product {self.name}>"
    
# ==========================================================
# Customer Model
# This model stores customer information used
# during billing and customer management.
# ==========================================================

class Customer(db.Model):
    """
    Store customer information.
    """

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Customer Full Name
    name = db.Column(
        db.String(100),
        nullable=False
    )

    # Customer Mobile Number
    mobile = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )

    # Customer Email Address
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )

    # Customer Address
    address = db.Column(
        db.Text,
        nullable=True
    )

    def __repr__(self):
        """
        Display customer information.
        """
        return f"<Customer {self.name}>"