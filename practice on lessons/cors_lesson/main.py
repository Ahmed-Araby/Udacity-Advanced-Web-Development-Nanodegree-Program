from models import setUpDataBase, books, db
from books_model import *
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from error_handlers import setUpErrorHandlers

app = Flask(__name__);
app.config.from_object('config');
CORS(app);
setUpDataBase(app);
setUpErrorHandlers(app);


# route handlers
@app.route('/')
def index():
    return "hellow";

@app.route('/books')
def get_books(): # with pagination
    start_id = request.args.get('id', 1, int);
    limit  = 5;

    records = get_books_paginate_db(start_id, limit);
    result = [];

    for rec in records:
        result.append(rec.format());

    return jsonify({
        "success":True,
        "status_code":200,
        "books": result
    });

@app.route('/books/<int:book_id>')
def get_book(book_id):
    """
        I guess it's better to take all the decision for abort here
    """

    bookObj = get_book_db(book_id);
    if bookObj == None:
        abort(404);
    return jsonify({
        "success":True,
        "book":bookObj.format()
    });


"""
the actions of the end point 
is defined by the method it handles
"""

@app.route('/books/<int:book_id>', methods=['delete'])
def delete_book(book_id):
    result  = delete_book_db(book_id);
    if result['success'] == False:
        abort(result['error']);
    return jsonify(result);


@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book_partial(book_id):
    body = request.get_json(); # this will respond with 400 automatically
    if ("category" in body) == False:
        abort(400);
    category = body.get('category', 1);
    result = update_book_categeory_db(book_id, category);
    if result['success'] == False:
        abort(result['error']);

    return result

@app.route('/books', methods=['POST'])
def create_book():
    body = request.get_json();
    if not("name" in body) or not("category" in body):
        abort(400);

    result = create_book_db(body);
    if result['success'] == False:
        abort(500); # server error

    return jsonify({
        "success":True,
        "newBookId":result['newBookId']
    });

# end points for searching

@app.route('/books/search', methods = ['POST'])
def search_books():
    body = request.get_json();
    if "search_category" in body == False:
        abort(400);

    success , records = search_books_with_cat(body['search_category']);
    if not success:
        abort(500);

    result = {"success":True,
              "total_matched":len(records),
              "status_code":200};
    matched_books = [];
    for record in records:
        matched_books.append(record.format());
    result['matched_books'] = matched_books;
    return jsonify(result);

#app.run(debug=True);