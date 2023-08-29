import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# connecting to MongoDB Atlas cloud database
cluster = os.getenv("DATABASE_URL")
client = MongoClient(cluster)
db = client["IDS_TEST"]

# importing routes
from routes.homePage import homePage
from routes.ipScan import ipScan
from routes.portScan import portScan
from routes.cveScan import cveScan
from routes.serviceScan import serviceScan
from routes.dosAttack import dosAttack
from routes.ddosAttack import ddosAttack


app = Flask(__name__) # creating flask app
CORS(app, resources={r"/*":{'origins':"*"}})

# registering blueprints for routes
app.register_blueprint(homePage)
app.register_blueprint(ipScan)
app.register_blueprint(portScan)
app.register_blueprint(cveScan)
app.register_blueprint(serviceScan)
app.register_blueprint(dosAttack)
app.register_blueprint(ddosAttack)
