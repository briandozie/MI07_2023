from flask import Blueprint, jsonify, request, current_app
import jwt
import os

checkAuthRoute = Blueprint("checkAuthRoute", __name__, url_prefix="/check-auth")

@checkAuthRoute.get("/")
def checkAuthenticationStatus():
    # Checks to see if "token" cookie is present in the request
    token = request.cookies.get("token")
    secret_key = os.getenv("SECRET_KEY")

    current_app.logger.debug(f"Received token: {token}")

    if token:
        # Decode and verify the token to ensure its valid
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])

            # If token is valid, then user is authenticated
            current_app.logger.info("User is authenticated (auth.py)")
            return jsonify(message="User is authenticated"), 201
        
        except jwt.ExpiredSignatureError:
            current_app.logger.warning("Token has expired")
            return jsonify(message="Token has expired"), 401
        
        except jwt.InvalidTokenError as e:
            current_app.logger.error(f"Invalid token: {e}")
            return jsonify(message="Invalid token"), 401
        
    else:
        # If there is no token then user is not authenticated
        current_app.logger.info("User is not authenticated")
        return jsonify(error="User is not authenticated"), 401