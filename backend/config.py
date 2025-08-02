# contains the main configuration of our application 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# initializes the flask application
app = Flask(__name__)
# wrap the app in CORS, disabling the error
CORS(app)

# initialize database things
# specify the location of the file (local sqlite database) we are storing on this machine
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
# Means we aren't gonna track all the modifications we make to the database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create an instance of the database, which gives us access to the database specified earlier so that we can CRUD
db = SQLAlchemy(app)


