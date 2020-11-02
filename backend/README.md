# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
**Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
env/Scripts/activate
```


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


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:

    {
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }

The API returns three types of errors:

* 400 – Bad Request
* 404 – Resource Not Found
* 422 – Unprocessable Entity

### Endpoints

##### GET /categories

* Returns a list categories.
* Example: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "success": true
        }


##### GET /questions

* General:
  * Returns list of questions.
  * Results are paginated in groups of 10.
  * Also returns list of categories and total number of questions.
* Example: `curl http://127.0.0.1:5000/questions`

            {
               "categories":{
                  "1":"Science",
                  "2":"Art",
                  "3":"Geography",
                  "4":"History",
                  "5":"Entertainment",
                  "6":"Sports"
                },
           "questions":[
           {
                 "answer":"Maya Angelou",
                 "category":4,
                 "difficulty":2,
                 "id":5,
                 "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
                 "answer":"Muhammad Ali",
                 "category":4,
                 "difficulty":1,
                 "id":9,
                 "question":"What boxer's original name is Cassius Clay?"
          },
          .....
          ],
       "success":true,
       "total_questions":21
    }

##### DELETE /questions/\<int:id\>
* Deletes a question by id using url parameters.
* Returns id of deleted question upon success.
* Example: `curl http://127.0.0.1:5000/questions/1 -X DELETE`

        {
            "deleted": 1, 
            "success": true
        }

##### POST /questions

This endpoint creates a new question or returns a search results based on aquery.

1. If no search term is passed in request:
      * Creates a new question using JSON request parameters.
      * Returns JSON object with newly created question, as well as paginated questions.
* Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            'question': 'Who is the director of the movie Parasite?',
            'answer': 'Bong Joon-ho',
            'difficulty': 1,
            'category': '5'
        }'`

        {
            "created": 26, 
            "question_created": "Who is the director of the movie Parasite?", 
        questions":[
        {
            "answer":"Maya Angelou",
             "category":4,
             "difficulty":2,
             "id":5,
             "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
             "answer":"Muhammad Ali",
             "category":4,
             "difficulty":1,
             "id":9,
             "question":"What boxer's original name is Cassius Clay?"
        },
        .......
       ],
           "success":true,
           "total_questions":20
        }


2. If searchterm is passed in request:
      * Searches for questions using search term in JSON request parameters.
      * Returns JSON object with paginated matching questions.
* Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "what"}'`
        
        {
           "questions":[
              {
                 "answer":"Muhammad Ali",
                 "category":4,
                 "difficulty":1,
                 "id":9,
                 "question":"What boxer's original name is Cassius Clay?"
              },
              {
                 "answer":"Apollo 13",
                 "category":5,
                 "difficulty":4,
                 "id":2,
                 "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
              },
              ......
           ],
           "success":true,
           "total_questions":19
        }

##### GET /categories/\<int:id\>/questions
      * Gets questions by category id using url parameters.
      * Returns JSON object with paginated matching questions.
* Example: `curl http://127.0.0.1:5000/categories/1/questions`

        {
           "current_category":"Science",
           "questions":[
              {
                 "answer":"The Liver",
                 "category":1,
                 "difficulty":4,
                 "id":20,
                 "question":"What is the heaviest organ in the human body?"
              },
              {
                 "answer":"Alexander Fleming",
                 "category":1,
                 "difficulty":3,
                 "id":21,
                 "question":"Who discovered penicillin?"
              },
              {
                 "answer":"Blood",
                 "category":1,
                 "difficulty":4,
                 "id":22,
                 "question":"Hematology is a branch of medicine involving the study of what?"
              }
           ],
           "success":true,
           "total_questions":19
        }
##### POST /quizzes
      * Allows users to play the quiz game.
      * Returns JSON object with random question not among previous questions.
* Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 4],"quiz_category": {"type": "Entertainment", "id": "5"}}'`

        {
            "question": {
                "answer": "Edward Scissorhands", 
                "category": 3, 
                "difficulty": 4, 
                "id": 6, 
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }, 
            "success": true
        }
