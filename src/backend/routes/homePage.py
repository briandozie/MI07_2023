from flask import Blueprint, session

homePage = Blueprint("homePage", __name__, url_prefix="/home")

@homePage.get("/")
def home():
    if (session['token'] is None): 
        return "Unauthenticated!"
    else:
        return "Hello Flask!"