from flask import Blueprint

homeBp = Blueprint("/", __name__)

@homeBp.route("/", methods=["GET"])
def testMethod():
    return "Hello Flask!"