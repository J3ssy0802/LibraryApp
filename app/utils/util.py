from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "a super secret, secret key"

def encode_token(member_id): #using unique pieces of info to make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), #setting the expiration time for the token to be 1 hour from now
        'iat': datetime.now(timezone.utc), #setting the issued at time for the token to be now
        'sub': str(member_id) #this needs to be a string because the jwt library expects it to be a string
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Look for the token in the Authorization header.
        if 'Authorization' not in request.headers:
            return jsonify({'message': 'Authorization header is missing!'}), 401

        token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token to get the member_id.
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            member_id = data['sub']
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(member_id, *args, **kwargs)

    return decorated