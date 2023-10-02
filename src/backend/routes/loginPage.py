from flask import Blueprint, request, jsonify, make_response, session
from pymongo import MongoClient
from app import db

loginPage = Blueprint("loginPage", __name__, url_prefix="/login")

@loginPage.post("/")
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = getUser(username, password)

    if user:
        # Generate token for authenticated user
        token = "cookie123"
        session['token'] = token

        # Set HTTP-only cookie
        response = make_response(jsonify(message="Login Successful"))
        response.set_cookie('authToken', token, httponly=True, secure=True)
    
        return response, 200
        # return jsonify(message="Login Successful")

    else:
        # In case of failed login, display error message and return
        # a 401 unauthorised status code
        return jsonify(error="Invalid username or password"), 401 

def getUser(username, password):
    users_collection = db["user"]
    user = users_collection.find_one({
        "username" : username,
        "password" : password,
    })
    return user