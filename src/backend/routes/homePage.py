from flask import Blueprint

homePage = Blueprint("homePage", __name__, url_prefix="/home")

@homePage.get("/")
def home():
    return "Hello Flask!"