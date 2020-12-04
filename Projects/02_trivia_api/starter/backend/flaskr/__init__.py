import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from error_handlers import setUpErrorHandlers
import random
from models import setup_db, Question, Category
from models import db
from sqlalchemy import func

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # cors
    # for each resource define the origins that are allowed to
    # make CORS on this origin.
    CORS(app, resources={"*":{"origins":"*"}});
    @app.after_request
    def after_request(response):
      """
      add headers to the response to tell the browser about the
      allowed headers and methods
      :param response:
      :return: response with the additional headers
      """
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
      return response;

    # end points -- categories resource

    @app.route('/categories')
    def get_categories():
      categories = None;
      try:
        categories = db.session.query(Category).all();
      except:
        abort(500);
      finally:
        db.session.close();

      cats_formated = {};
      for cat in categories:
        cats_formated[cat.id] = cat.type;
      return jsonify({
            "categories":cats_formated
      });

    @app.route('/questions')
    def get_questions_pagination():
        pageNumber = request.args.get('page', 1, int);
        categories = [];
        questions = [];

        try:
            questions = db.session.query(Question).order_by(Question.id).all();
            categories = db.session.query(Category).all();
        except:
            abort(500);
        finally:
            db.session.close();


        startIndex = (pageNumber - 1) * QUESTIONS_PER_PAGE;
        endIndex = min(startIndex + QUESTIONS_PER_PAGE, len(questions));  # excluded
        if endIndex <= startIndex:
            abort(404);

        # format the data for the frontEnd
        index = 0
        categoriesList = {};
        for cat in categories:
            categoriesList[cat.id] = cat.type;
            index +=1;
        index = 0
        for q in questions:
            questions[index]  = q.format();
            index +=1;
        return jsonify({
            "questions": questions[startIndex:endIndex],
            "total_questions":len(questions),
            "categories":categoriesList,
            "current_category":""
        });

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        question = None;
        affectedRowsCount = 0;
        try:
            affectedRowsCount = Question.query.filter(Question.id == question_id).delete()
            db.session.commit();
        except:
            abort(500);
        finally:
            db.session.close();

        if affectedRowsCount == 0:
            abort(404);
        return jsonify({
            "success":True,
            "status_code":200,
            "message": "question with id {} have been deleted successfully".format(question_id)
        });

    @app.route('/questions', methods=['POST'])
    def add_questions():

        """
            I should do validation on the data
            SQLAlchemy protect us from SQL injection
        """
        newQuestionId = -1;
        try:
            """
            catch the failure of having non 
            json data, and data base failure
            """
            data = request.get_json();
            newQuestion = Question(**data);
            db.session.add(newQuestion);
            db.session.commit();
            newQuestionId = newQuestion.id;
        except:
            abort(500);
        finally:
            db.session.close();

        """
            if this was a real API that would 
            go into the production I won't send back all this info 
            on success
        """

        return jsonify({
            "success":True,
            "status_code":200,
            "message":"new Question with id {} had been added successfuly".format(newQuestionId),
            "new_question_id":newQuestionId
        });

    @app.route('/questions/search', methods = ['POST'])
    def search_questions():
        data = request.get_json();
        if not ("searchTerm" in data):
            abort(400)
        searchTerm = "%" + data['searchTerm'].lower() + "%";    # convert it into expression.
        try:
            """
            case insensitive search 
            """
            questions = db.session.query(Question).filter(func.lower(Question.question).like(searchTerm)).order_by(Question.id).all();
        except:
            abort(500);
        finally:
            db.session.close();

        # format the data
        index = 0;
        for q in questions:
            questions[index] = q.format();
            index +=1;
        return jsonify({
            "questions":questions,
            "total_questions":len(questions),
            "current_category":""
        });


    @app.route('/categories/<int:cat_id>/questions')
    def get_questions_of_category(cat_id):
        questions  = [];
        category_type = None; # if not declared here Would I be able to access it outside the try !! ??

        # get the category Type as string, also make sure that it exists.
        try:
            category_type = db.session.query(Category.type).filter(Category.id == cat_id).one_or_none();
        except Exception as e:
            print("error in get_questions_of_category : category_type", e);
            abort(500);
        finally:
            db.session.close();
        if category_type == None:
            abort(404);
        category_type = category_type[0];

        # get questions of this category.
        try:
          questions = db.session.query(Question).filter(Question.category == cat_id).order_by(Question.id).all();
        except Exception as e:
          print("error in get_questions_of_category : questions", e);
          abort(500);
        finally:
          db.session.close();

        # format the data for the frontEnd.
        questionsList = [];
        for q in questions:
          questionsList.append(q.format());
        return jsonify({
          "current_category":category_type,
          "total_questions":len(questionsList),   # all questions or regardless of the category
                                                # or only questions that beling to required category
          "questions":questionsList
        });

    @app.route('/quizzes', methods = ["post"])
    def quiz_next_question():
        data = request.get_json();
        nextQuestion = None;
        print("quizz data : ", data);
        # validate json data.
        if not("previous_questions" in data
               and "quiz_category" in data
               and len(data['quiz_category']) == 2):
            abort(400);

        prevQuestionsIds = data.get('previous_questions');
        quizCatId = data.get('quiz_category')['id'];

        try:
            questionsQuery = db.session.query(Question).filter(Question.id.notin_(prevQuestionsIds));
            if quizCatId !=0: # not All category
                questionsQuery = questionsQuery.filter(Question.category == quizCatId);
            nextQuestion  = questionsQuery.first(); # could be None
        except:
            abort(500);
        finally:
            db.session.close();

        if nextQuestion !=None:
            nextQuestion = nextQuestion.format();
        return jsonify({
           "question":nextQuestion
        });

    return app


if __name__ == "__main__":
  app = create_app()
  setUpErrorHandlers(app);
  app.run(debug=True)
