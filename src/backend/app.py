from flask import Flask
from pymongo import MongoClient

# importing routes
from routes.home import homeBp
from routes.test import testBp

# connecting to MongoDB Atlas cloud database
cluster = "mongodb+srv://developer:XtaPr43DKO729pfm@idstest.7xzpnqp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.IDS_TEST

app = Flask(__name__) # creating flask app

# registering blueprints for routes
app.register_blueprint(homeBp)
app.register_blueprint(testBp)

# run app
if __name__ == "__main__":
    app.run(debug=True)