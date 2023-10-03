from flask import jsonify, session

def checkAuthenticationStatus():
    if session.get("authenticated"):
        return jsonify(authenticated = True, username = session.get("username"))
    else:
        return jsonify(authenticated = False)