from models import books, db
from flask import abort

def get_books_db():
    return db.session.query(books).all();

def get_books_paginate_db(start_id, limit):
    records = [];
    try:
        records = db.session.query(books).filter(books.id >= start_id).limit(limit).all();
    except:
        abort(500); # server error as the Data base is not available
    finally:
        db.session.close();
    return records

def get_book_db(book_id):
    book_obj = None;
    error = False;

    try:
        book_obj = db.session.query(books).filter(books.id == book_id).one_or_none();
    except:
        error = True;
    finally:
        db.session.close();
    if error:
        abort(500);
    return book_obj;

def create_book_db(data):
    name = data['name'];
    category = data['category'];
    newBook = books(name=name, category = category);
    success = True
    newBookId = -1;
    try:
        db.session.add(newBook);
        db.session.commit();
        newBookId = newBook.id; # could fail as newBook is supposed to expire !!!???
    except:
        db.rollback();
        success = False;
    finally:
        db.session.close();

    return {
        "success":success,
        "newBookId":newBookId
    };

def delete_book_db(book_id):
    result = {"success":True};
    try:
        bookObj = db.session.query(books).filter(books.id == book_id).one_or_none();
        if bookObj == None:
            result['success'] = False;
            result['error'] = 404;
        else:
            db.session.delete(bookObj);
            db.session.commit();
    except:
        db.session.rollback(); # what if there is no action had been taken !?
        result['success'] = False;
        result['error'] = 500;
    finally:
        db.session.close();

    return result;

def update_book_categeory_db(book_id, newCategory):
    result = {"success":True};
    try:
        bookObj = db.session.query(books).filter(books.id == book_id).one_or_none();
        if bookObj == None:
            result['success'] = False;
            result['error'] = 404;
        else:
            bookObj.category = newCategory;
            db.session.commit();
    except:
        db.session.rollback();
        result['success'] = False;
        result['error'] = 500;
    finally:
        db.session.close();

    return result;

def search_books_with_cat(category):
    success = True;
    result = [];

    try:
        result = db.session.query(books).filter(books.category == category).all();
    except:
        success = False;
    finally:
        db.session.close();

    return (success, result);