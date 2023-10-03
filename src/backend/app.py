import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from pymongo import MongoClient

# connecting to MongoDB Atlas cloud database
cluster = os.getenv("DATABASE_URL")
client = MongoClient(cluster)
db = client["IDS_TEST"]

# importing routes
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
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "testing"
app.secret_key = b'j60e04te6ze77d35xg' # Added secret key (needs to be changed)

Session(app)
CORS(app, resources={r"/*":{'origins':"*"}})

# registering blueprints for routes
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