from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from app import db
import jwt
import datetime

loginPage = Blueprint("loginPage", __name__, url_prefix="/login")

@loginPage.post("/")
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = getUser(username, password)

    if user:
        # Generate a token
        token = generateToken(username)

        # Return the token in response
        return jsonify(message="Login Successful", token=token), 200

    else:
        # In case of failed login, display error message and return
        # a 401 unauthorised status code
        return jsonify(error="Invalid username or password"), 401 

def generateToken(username):
    secret_key = "CCP2023mi07"

    # Token expires in 1 hour
    expiration = datetime.timedelta(hours=1)

    # Create payload with username and expiration time
    payload = {
        "user_id": str(username),
        "exp": datetime.datetime.utcnow() + expiration
    }

    # Generate the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token

def getUser(username, password):
    users_collection = db["user"]
    user = users_collection.find_one({
        "username" : username,
        "password" : password,
    })
    return user