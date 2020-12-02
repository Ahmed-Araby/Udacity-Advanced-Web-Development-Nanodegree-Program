from main import *
import json

import unittest

class books_getAllBooks(unittest.TestCase):
    def setUp(self):
        print("inside setUP");
        self.client = app.test_client;  # what is this !!???

        for i in range(0, 3):
            bookObj = books(name='book'+ str(i), category='algorithm', rank=1);
            db.session.add(bookObj);

        for i in range(0, 3):
            bookObj = books(name='book' + str(i), category='operating systems', rank=2);
            db.session.add(bookObj);

        db.session.commit();

    def tearDown(self):
        print("inside tearDown");
        db.session.query(books).delete();
        db.session.commit();

    # test get all books endPoint.
    def test_getAllBooks(self):
        res = self.client().get('/books'); # simulate get request
        data = json.loads(res.data);
        self.assertEqual(res.status_code, 200);
        self.assertEqual(data['success'], True);
        self.assertEqual(data['status_code'], 200);
        if len(data['books']) == 0:
            self.assertEqual(True, False);

    """
    500 fail the whole test process
    def test_500_getAllBooks(self):
        res = self.client().get('/books');
        data = json.loads(res.data);
        self.assertEqual(res.status_code, 500);
        self.assertEqual(data['success'], False);
        self.assertEqual(data['error_code'], 500);
        return ;
    """

    # test update endpoint
    def test_updateBook(self):
        bookObj = db.session.query(books).order_by(books.id).first();
        bookObj.category = 'not a known type';
        db.session.commit();
        editedBookObj = db.session.query(books).order_by(books.id).first();
        self.assertEqual(editedBookObj.category,'not a known type' );
        return ;


    # test search end point
    def test_searchWithResults(self):
        res = self.client().post('/books/search', json={'search_category':'algorithm'});
        data = json.loads(res.data);
        self.assertEqual(res.status_code, 200);
        self.assertEqual(data['status_code'], 200);
        self.assertEqual(data['success'], True);
        self.assertEqual(data['total_matched'], 3);
        self.assertEqual(len(data['matched_books']), 3);
        return ;

    def test_searchWithOutResults(self):
        res = self.client().post('/books/search', json={'search_category':'algorthm233232'});
        data = json.loads(res.data);
        self.assertEqual(res.status_code, 200);

        self.assertEqual(res.status_code, 200);
        self.assertEqual(data['status_code'], 200);
        self.assertEqual(data['success'], True);
        self.assertEqual(data['total_matched'], 0);
        self.assertEqual(len(data['matched_books']),0);
        return ;

print(__name__);
unittest.main();
