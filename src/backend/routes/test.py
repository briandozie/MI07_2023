from flask import Blueprint

testBp = Blueprint("test", __name__, url_prefix="/test")

@testBp.route("", methods=["GET"])
def testMethod():
    return "Sample text for testing"