import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

"""
400 bad request , malformed request syntax.
401 unauthorized
403 forbiden
404 not found
500 server error
200 okay
"""

# get information from env
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN ','fsnd-ahmed.us.auth0.com');
ALGORITHMS = [os.getenv('ALGORITHMS ', 'RS256')];
API_AUDIENCE = os.getenv('API_AUDIENCE','coffee');

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
[Done]
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    headers = request.headers

    if "Authorization" not in headers:
        raise AuthError({"code": "authorization error",
                         "description": "authorization header is not exist"}, 401)

    auth_header = headers['Authorization']
    parts = auth_header.split(' ')

    # check for the validaty of the auth header
    if len(parts) != 2:
        raise AuthError({"code": "not supported authorization type",
                         "description": "authorization header have to be of type bearer"}, 400)
    type = parts[0]
    token = parts[1]
    if type.lower() != "bearer":
        raise AuthError({"code": "not supported authorization type",
                         "description": "authorization header have to be of type bearer"}, 400)

    return token


'''
[Done]
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if permission == "":
        return True

    if "permissions" not in payload:
        raise AuthError({"code": "invalid token payload",
                         "description": "malformed payload, there is no permissions array"},
                        400)

    if permission not in payload['permissions']:
        raise AuthError({"code": "forbidden",
                         "description": "un authorized to use this resourse"}, 401)

    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # get keys
    jsonUrl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    keys = json.loads(jsonUrl.read())

    # get the header
    un_verifiedHeader = jwt.get_unverified_header(token)
    if "kid" not in un_verifiedHeader:
        raise AuthError(
            {
                "code": "invalid token header",
                "description": "invalid header, token is malformed there os no kid"},
            400)

    # match kid to
    rsa_key = {}
    for key in keys['keys']:
        if key['kid'] == un_verifiedHeader['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if not rsa_key:
        raise AuthError({"code": "invalid token header",
                         "description": "cant find the appropriate key to verify the token"},
                        401)

    # use the key to verify the token.
    payload = None
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer="https://" + AUTH0_DOMAIN + "/"
        )

    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired",
                         "description": "token is expired"}, 401)
    except jwt.JWTClaimsError:
        raise AuthError({"code": "invalid_claims",
                         "description":
                             "incorrect claims,"
                             " please check the audience and issuer"}, 401)
    except Exception:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Unable to parse authentication"
                             " token."}, 401)
    return payload


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            payload = None

            # thrown wxception will be handled by the flask error handler
            token = get_token_auth_header()  # get token from the request object
            # verify the token, if valid decode it and return
            payload = verify_decode_jwt(token)
            # check the required permission for the current resource
            check_permissions(permission, payload)

            # call the handler function with the payload, in case we need any
            # user related info
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator