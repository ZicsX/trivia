import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# paginate questions


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    # error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = {
            category.id: category.type for category in Category.query.all()}

        if not len(categories):
            abort(404)
        return jsonify({'success': True, 'categories': categories}), 200

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        total_questions = len(questions)
        current_questions = paginate(request, questions)

        if not len(current_questions):
            abort(404)

        categories = {
            category.id: category.type for category in Category.query.all()}

        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'categories': categories,
            'questions': current_questions

        }), 200

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({'success': True, 'deleted': id})

        except:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.

    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods=['POST'])
    def post_questions():
        response = request.get_json()

        search_term = response.get('searchTerm')
        if (search_term):
            search = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")).all()

            total_questions = len(search)
            if not total_questions:
                abort(404)

            current_questions = paginate(request, search)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': total_questions
            }), 200
        # Post new question
        else:

            question = response.get('question')
            answer = response.get('answer')
            difficulty = response.get('difficulty')
            category = response.get('category')

            if not(question and answer and category and difficulty):
                abort(422)

            try:
                new_question = Question(question=question, answer=answer,
                                        category=category, difficulty=difficulty,)
                new_question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate(request, selection)

                return jsonify({
                    'success': True,
                    'created': new_question.id,
                    'question': new_question.question,
                    'total_questions': len(Question.query.all())
                }), 200

            except:
                abort(422)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_on_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()

        if not len(questions):
            abort(404)

        total = len(Question.query.all())
        paginated_questions = paginate(request, questions)

        return jsonify({
            'success': True,
            'total_questions': total,
            'current_category': category_id,
            'questions': paginated_questions
        }), 200

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def quizzes():

        response = request.get_json()
        category = response.get('quiz_category')
        previous_questions = response.get('previous_questions')

        if ((category is None) or (previous_questions is None)):
            abort(400)
        if not (category['id']):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        if len(questions) == len(previous_questions):
            return jsonify({
                'success': True
            }), 200

        for previous in previous_questions:
            for question in questions:
                if question.id == previous:
                    questions.remove(question)
                    break

        random.shuffle(questions)
        question = questions[random.randrange(0, len(questions), 1)]

        return jsonify({'success': True, 'question': question.format()}), 200

    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run()
