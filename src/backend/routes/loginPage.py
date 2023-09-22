from flask import Blueprint, request, jsonify, make_response
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
        #response = make_response(jsonify(message="Login Successful"))
        return jsonify(message="Login Successful")
        #response.set_cookie('authToken', value=auth_token, httponly=True, secure=True)
        #return response
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