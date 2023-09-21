from flask import Blueprint, request, redirect, session, jsonify
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
        # Create session with username upon successful login
        session["username"] = username
        return jsonify(message="Login Successful")
    else:
        # In case of failed login, display error message and return
        # a 401 unauthorised status code
        return jsonify(error="Invalid username or password"), 401 

def getUser(username, password):
    users_collection = db["user"]
    x = users_collection.find_one({
        "username" : username,
        "password" : password,
    })
    return x["user"]