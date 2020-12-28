import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

# changing the relative import to absolute import.
from src.database.models import db_drop_and_create_all, setup_db, Drink, db
from src.auth.auth import AuthError, requires_auth
from src.database.drinksModel import *
from src.error_handlers import *

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
I don't fully understand why do I need
this line,  or why I am getting the error that it solve when I use jsonify
"""
app.app_context().push()

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint -- no auth needed
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    try:
        drinks = getDrinks()
    except BaseException:
        abort(500)
    return jsonify({"success": True, "drinks": drinks})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    """
    if we had an error in the decorator[wrapper] the code flow will not
    make it till here which mean except clause will not handle this error and
    this error will propogate to error_handler of flask
    as this view function is called by the wrapper
    """

    try:
        drinks = getDrinksDetails()
    except Exception:
        abort(500)

    return jsonify({"success": True, "drinks": drinks})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=["POST"])
@requires_auth('post:drinks')
def insert_drink(payload):
    newDrink = request.get_json()  # what if the data is not json
    response = insertDrink(newDrink)
    if response['success']:
        return jsonify({"success": True, "drink": response['drink'].long()})
    else:
        """
        we will be able to tell the user if the problem
        is in viloating unique constrain or just server error.
        """
        abort(response['status_code'], response['error'])


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    # payload have to be the first,
    # the wrapper function will pass the id after the payload in order

    data = request.get_json()
    response = patchDrink(id, data)
    if not response['success']:
        abort(response['status_code'])

    return jsonify({"success": True, "drinks": [response['drink'].long()]})


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    response = deleteDrink(id)

    if not response['success']:
        abort(response['status_code'])

    return jsonify({"success": True, "delete": id})


setup_errorHandlers(app)
#app.run(debug=True)
