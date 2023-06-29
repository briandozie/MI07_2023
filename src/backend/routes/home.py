from flask import Blueprint

home = Blueprint("/", __name__)

@home.get("/")
def testMethod():
    return "Hello Flask!"