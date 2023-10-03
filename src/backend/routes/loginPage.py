from flask import Blueprint, request, jsonify, session, redirect, url_for
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
        #Perform user authentication by setting a session variable
        session['authenticated'] = True
        session['username'] = username
        
        return jsonify(message="Login Successful"), 200

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

@loginPage.route("/logout", methods=["GET"])
def logout():
    # Clear the session and log the user out
    session.clear()
    return redirect(url_for("loginPage.login"))