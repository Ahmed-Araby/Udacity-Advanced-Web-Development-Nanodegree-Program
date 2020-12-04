# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
# API Reference

## getting Started
* Base Url: your localhost and port for flask server.
* no Authentication, this is a simple API for learning perpouse.

## Error Handling
this API handle (404, 500, 400, 422) errors.

errors are returned as JSON objects in the following format:

```
{
    "success":False,
    "status_code":500,
    "message":"server error please try again later"
}
```
error types:

* 400: Bad Request (server can not deal with the format of the incomming data)
* 500: server error (data base failure or flask server failure).
* 422: Unprocessable Entity
* 404: Not Found: there is no resources for the requested URL.

## Endpoints


GET /categories

* General
    * returns all the categories stored in the database
    * returns the Id as key and the name of the categorie as the value
    
* Sample curl http://127.0.0.1:5000/categories

* Response 

```
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```

GET /questions

* General
    * returns paginated questions, max 10 questions per page.
    * returns total number of questions in the data base, list of at most 10 questions,
      and list dictionary of all the categories in the data base
    * take variable parameter that represents the front end page number
    
* Sample curl http://127.0.0.1:5000/questions?page=1

* Response 

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "",
  "questions": [
    {
      "answer": "ww",
      "category": 1,
      "difficulty": 5,
      "id": 27,
      "question": "w"
    },
    {
      "answer": "Ahmed",
      "category": 2,
      "difficulty": 5,
      "id": 28,
      "question": "what is your name"
    },
    {
      "answer": "W",
      "category": 1,
      "difficulty": 1,
      "id": 29,
      "question": "W"
    }
  ],
  "total_questions": 23
}
```

POST /questions

* General
    * add new Question to the data base 
    * incomming arguments are 
        * question 
        * answer 
        * category
        * difficulty
        
* Sample curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"what is your name", "answer":"Ahmed Araby", "difficulty":"5", "category":"1"}'

* Response 

```
{
  "message": "new Question with id 30 had been added successfuly",
  "new_question_id": 30,
  "status_code": 200,
  "success": true
}
```

Delete /questions/<question_id>

* General
    * delete a specific question  
    * URL has the question id as argument.
        
* Sample curl -X delete http://127.0.0.1:5000/questions/6

* Response 

```
{
  "message": "question with id 6 have been deleted successfully",
  "status_code": 200,
  "success": true
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
