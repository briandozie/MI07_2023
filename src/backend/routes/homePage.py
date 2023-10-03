from flask import Blueprint, session, redirect, url_for

homePage = Blueprint("homePage", __name__, url_prefix="/home")

@homePage.get("/")
def home():
    if not session.get("authenticated"):
        return redirect(url_for("loginPage.login"))
    else:
        return "Hello Flask!"