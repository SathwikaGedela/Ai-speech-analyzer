import os

# Get the absolute path to the backend directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database path should be in the backend directory
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False