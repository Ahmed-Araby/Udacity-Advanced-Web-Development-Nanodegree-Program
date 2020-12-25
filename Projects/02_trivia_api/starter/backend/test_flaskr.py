import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
# my imports
from models import db
from error_handlers import setUpErrorHandlers
from sqlalchemy import func


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        setUpErrorHandlers(self.app)  # add by me

        """
        # before using environment variable 
        self.database_name = "trivia_test";
        self.database_path = "postgres://postgres:0173706505aA@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app);
        """

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_getCategories(self):
        """
            should I use hard coded values to check against
            or query the dataBase to check the results against the API results.
        """
        # get data from the API
        res = self.client().get('/categories')
        data = json.loads(res.data)
        cats = data['categories']

        # get data form the data base
        catRowsCount = Category.query.count()

        # assert
        self.assertEqual(len(cats), catRowsCount)
        return

    def test_getQuestions_page_exist(self):
        # there is enough questions to fill this page
        # get dat from the API
        pageNumber = 1
        res1 = self.client().get('/questions?page=' + str(pageNumber))
        data1 = json.loads(res1.data)
        res2 = self.client().get('/categories')
        data2 = json.loads(res2.data)

        # get data from the data base
        qRowCount = Question.query.count()

        # assert
        self.assertLessEqual(len(data1['questions']), 10)
        self.assertEqual(data1['total_questions'], qRowCount)
        self.assertEqual(data1['categories'], data2['categories'])
        return

    def test_getQuestions_page_notExist(self):
        # there is no enough questions to reach this page
        # get data form the API
        pageNumber = 105
        res = self.client().get('/questions?page=' + str(pageNumber))
        data = json.loads(res.data)

        # assert
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['success'], False)
        return

    def test_getQuestions_byCategory_exist(self):
        # category exist

        # get data from the Data base
        catId = db.session.query(Question.category).first()[0]
        QCount = Question.query.filter(Question.category == catId).count()
        current_category_type = db.session.query(
            Category.type).filter(
            Category.id == catId).one_or_none()[0]

        # get data from the API
        URL = "/categories/{}/questions".format(catId)
        res = self.client().get(URL)
        data = json.loads(res.data)

        # assert, Hard coded !!!!!!!!!!!!!!!11
        # only questions that belong to this category
        self.assertEqual(data['total_questions'], QCount)
        self.assertEqual(current_category_type, data['current_category'])
        return

    def test_getQuestions_byCategory_notExist(self):
        # category exist

        catId = -99
        current_category = db.session.query(
            Category.type).filter(
            Category.id == catId).one_or_none()
        self.assertEqual(current_category, None)

        URL = "/categories/{}/questions".format(catId)
        res = self.client().get(URL)
        data = json.loads(res.data)

        # only questions that belong to this category
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['success'], False)
        return

    def test_deleteQuestion(self):  # this will persist in the data base
        totalQCountBefore = Question.query.count()
        qId = db.session.query(Question.id).first()[0]

        # delete
        res = self.client().delete('/questions/' + str(qId))
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 200)

        totalQCountAfter = Question.query.count()
        self.assertEqual(totalQCountBefore, totalQCountAfter + 1)

        return

    # this test will affect the data base and persist on it.
    def test_addQuestion(self):
        totalQCountBefore = Question.query.count()
        res = self.client().post(
            '/questions',
            json={
                "question": "w",
                "answer": "ww",
                "difficulty": "5",
                "category": "1"})
        totalQCountAfter = Question.query.count()
        self.assertEqual(totalQCountAfter, totalQCountBefore + 1)
        return

    def test_questionsSearch(self):
        searchTerm = "%name%"
        questions = db.session.query(Question).filter(
            func.lower(
                Question.question).like(searchTerm)).order_by(
            Question.id).all()

        res = self.client().post(
            '/questions/search',
            json={
                "searchTerm": searchTerm})
        data = json.loads(res.data)

        index = 0
        for q in questions:
            questions[index] = q.format()
            index += 1
        self.assertEqual(questions, data['questions'])
        return

    def test_quizz_question(self):
        previous_Qs = [1, 15, 3, 25, 7]
        category_id = 1   # all
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": previous_Qs,
                "quiz_category": {
                    "type": "--",
                    "id": category_id}})
        data = json.loads(res.data)
        question = data['question']
        self.assertEqual(category_id, question['category'])
        self.assertTrue(not(question['id'] in previous_Qs))
        return


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
