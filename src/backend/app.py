import os
from flask import Flask
from pymongo import MongoClient

# importing routes
from routes.home import home
from routes.test import test
from routes.ipScan import ipScan

# connecting to MongoDB Atlas cloud database
cluster = os.getenv("DATABASE_URL")
client = MongoClient(cluster)
db = client.IDS_TEST

app = Flask(__name__) # creating flask app

# registering blueprints for routes
app.register_blueprint(home)
app.register_blueprint(test)
app.register_blueprint(ipScan)