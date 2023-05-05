from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# connecting to MongoDB Atlas cloud database
cluster = "mongodb+srv://developer:XtaPr43DKO729pfm@idstest.7xzpnqp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.IDS_TEST

# routes
@app.route("/", methods = ["GET"])
def home():
    return "Hello, Flask!"

# run
if __name__ == "__main__":
    app.run(debug=True)