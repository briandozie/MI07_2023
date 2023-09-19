from flask import Blueprint, request, redirect, session
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
        session(username)
        return redirect("/home")
    else:
        return redirect(location="/login", Response="Invalid username or password!")

def getUser(username, password):
    users_collection = db["user"]
    x = users_collection.find_one({
        "username" : username,
        "password" : password,
    })
    return x["user"]