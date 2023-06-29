from flask import Blueprint

test = Blueprint("test", __name__, url_prefix="/test")

@test.get("/")
def testMethod():
    return "Sample text for testing"