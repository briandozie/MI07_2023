from flask import Blueprint, request, jsonify, make_response
from pymongo import MongoClient
from app import db
import jwt
import datetime
import os
import bcrypt

loginPage = Blueprint("loginPage", __name__, url_prefix="/login")

@loginPage.post("/")
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = getUser(username)

    if user and verify_password(password, user['password']):
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
    secret_key = os.getenv("SECRET_KEY")

    # Token expires in 3 hour
    expiration = datetime.timedelta(hours=3)

    # Create payload with username and expiration time
    payload = {
        "user_id": str(username),
        "exp": datetime.datetime.utcnow() + expiration
    }

    # Generate the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token

def getUser(username):
    users_collection = db["user"]
    user = users_collection.find_one({
        "username" : username,
    })
    return user

def verify_password(provided_passwd, stored_passwd):
    match = bcrypt.checkpw(provided_passwd.encode('utf-8'), stored_passwd.encode('utf-8'))
    return match
    