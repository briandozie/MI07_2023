import os
from flask import Flask
from pymongo import MongoClient

# importing routes
from routes.home import home
from routes.test import test
from routes.ipScan import ipScan
from routes.portScan import portScan
from routes.cveScan import cveScan

# connecting to MongoDB Atlas cloud database
# Uncomment before Pull Request
'''
cluster = os.getenv("DATABASE_URL")
client = MongoClient(cluster)
db = client.IDS_TEST '''

app = Flask(__name__) # creating flask app

# registering blueprints for routes
app.register_blueprint(home)
app.register_blueprint(test)
app.register_blueprint(ipScan)
app.register_blueprint(portScan)
app.register_blueprint(cveScan)