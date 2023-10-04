import os
import logging
import sys
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# connecting to MongoDB Atlas cloud database
cluster = os.getenv("DATABASE_URL")
client = MongoClient(cluster)
db = client["IDS_TEST"]

# importing routes
from utilities.authenticate import checkAuthRoute # Import authentication
from routes.loginPage import loginPage
from routes.homePage import homePage
from routes.ipScan import ipScan
from routes.portScan import portScan
from routes.cveScan import cveScan
from routes.serviceScan import serviceScan
from routes.dosAttack import dosAttack
from routes.ddosAttack import ddosAttack
from routes.dashboard import dashboard

app = Flask(__name__) # creating flask app
CORS(app, resources={r"/*":{'origins':"*"}}, supports_credentials=True) #set to true to support cookies

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')

# registering blueprints for routes
app.register_blueprint(checkAuthRoute) # Added authentication route
app.register_blueprint(loginPage)
app.register_blueprint(homePage)
app.register_blueprint(ipScan)
app.register_blueprint(portScan)
app.register_blueprint(cveScan)
app.register_blueprint(serviceScan)
app.register_blueprint(dosAttack)
app.register_blueprint(ddosAttack)
app.register_blueprint(dashboard)

# if __name__ == "__main__":
#     app.run(host="192.168.6.22", port=5000)