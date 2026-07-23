"""
Super Mart Management System
----------------------------

Purpose:
This module creates a shared SQLAlchemy database object.
The database object is used throughout the project to
perform all database operations.

Author: Your Name
"""

from flask_sqlalchemy import SQLAlchemy


# Create a global SQLAlchemy instance.
# This object will be initialized inside the Flask application
# and shared across all modules that need database access.
db = SQLAlchemy()