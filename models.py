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

from datetime import datetime

class Product(db.Model):
    # Primary key for uniquely identifying each product
    id = db.Column(db.Integer, primary_key=True)

    # Stores the product name
    name = db.Column(db.String(100), nullable=False)

    # Stores the product category
    category = db.Column(db.String(100), nullable=False)

    # Stores the selling price of the product
    price = db.Column(db.Float, nullable=False)

    # Stores the available stock quantity
    stock = db.Column(db.Integer, nullable=False)

    # Stores the product image file name
    image = db.Column(db.String(255), nullable=True)

    # Stores the date and time when the product is created
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Automatically updates the date and time whenever the product is modified
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


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
    
class Invoice(db.Model):
    """
    Store invoice information.
    """

    # Primary Key
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Invoice Number
    bill_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # Customer Name
    customer_name = db.Column(
        db.String(100),
        nullable=False
    )

    # Grand Total
    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    # Invoice Creation Date
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        """
        Return invoice information.
        """

        return f"<Invoice {self.bill_number}>"