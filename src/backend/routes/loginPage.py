from flask import Blueprint, request, jsonify, make_response
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

        response = make_response(jsonify(message="Login Successful"), 200)
        response.set_cookie("token", token, httponly=True)
        # Return the token in response
        return response

    else:
        # In case of failed login, display error message and return
        # a 401 unauthorised status code
        return jsonify(error="Invalid username or password"), 401 

def generateToken(username):
    secret_key = "CCP2023mi07"

    # Token expires in 1 hour
    expiration = datetime.timedelta(hours=3)

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