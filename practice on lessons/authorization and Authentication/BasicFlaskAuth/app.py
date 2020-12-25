from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import base64

import math

app = Flask(__name__)

AUTH0_DOMAIN = "fsnd-ahmed.us.auth0.com";
ALGORITHMS = ['RS256']
API_AUDIENCE = "image";


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')   # request to get the public key
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)   # header and payload are not encrypted, only converted to base64
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:        # match key id from the my account with key id sent with the token.
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:      # key type RSA of RSA algorithm.
        try:
            payload = jwt.decode(  # authenticate the token, then if valid it returns the payload.
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'      # service/site that sent this token.
            )
            # return token
            return payload;

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({         # failure and neither one of the above exceptions, so the token is not authenticated.
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

# get decorator that can take parameter
def check_permission(permission, payload):
    print(payload);
    if permission == "":
        return True;
    elif "permissions" not in payload:
        raise AuthError("payload don't have permissions ", 400);
    elif permission not in payload['permissions']:
        raise AuthError("{} is not in permissions {}".format(permission, payload['permissions']), 403);

    return True;

def requires_auth(permission = ""):
    def requires_auth_decorator(f):  # decorater
        @wraps(f)
        def wrapper(*args, **kwargs):  # wraper
            """
            new added functionality
            """

            try:
                token = get_token_auth_header()
                print("got token");
                payload = verify_decode_jwt(token)
            except AuthError as err:
                print(err.error)
                abort(401)

            # access permission throw closure
            try:
                check_permission(permission, payload);
            except AuthError as err:
                print(err.error);
                abort(err.status_code);

            return f(payload, *args, **kwargs)  # wrapped function

        return wrapper
    return requires_auth_decorator   # decorator

"""
series of actions 
- header is the base function 
- require auth decorate it by doing some work 
    which is [getting the token from authorization header, then verifying this token and getting the payload]
    pay load will hold user specific data that will help  me to get it's data from the data  base.
- then app.route() will register the final decorated function.
"""

@app.route('/headers')
@requires_auth('post:images')
def headers(payload):
    """
    parts = token.split('.');
    header = parts[0];
    payload = parts[1];
    print(base64.b64decode(header));
    print("\n\n");
    payload +='==';
    print(base64.b64decode(payload));
    print(len(payload));
    """
    print("the user is authenticated and authorized to have the ability to post images");
    print(payload);
    return 'Access Granted'

@app.route('/index')
def index():
    return "";

app.run(debug=True);