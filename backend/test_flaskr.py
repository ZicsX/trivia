import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format(
            'zicsx:23321@localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # sample question
        self.new_question = {
            'question': 'Who is the director of the movie Parasite (2019) ?',
            'answer': 'Bong Joon-ho',
            'difficulty': 1,
            'category': '5'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):

        # get response and load data
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that total_questions and questions return data
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_questions_fail(self):

        # send request with bad page data, load response
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_question(self):

        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        q_id = question.id
        questions_before = Question.query.all()

        response = self.client().delete('/questions/{}'.format(q_id))
        data = json.loads(response.data)
        questions_after = Question.query.all()
        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], q_id)
        self.assertTrue(len(questions_before) - len(questions_after) == 1)
        self.assertEqual(question, None)

    def test_post_question(self):

        questions_before = Question.query.all()

        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        questions_after = Question.query.all()
        question = Question.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        self.assertIsNotNone(question)

    def test_post_question_fails(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        questions_after = Question.query.all()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(questions_after) == len(questions_before))

    def test_search_questions(self):

        response = self.client().post('/questions',
                                      json={'searchTerm': 'egyptians'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['id'], 23)

    def test_search_questions_fails(self):

        response = self.client().post('/questions',
                                      json={'searchTerm': 'abcdefghijk'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_get_questions_on_category(self):

        response = self.client().get('/categories/5/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 5)

    def test_get_questions_on_category_fails(self):

        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_get_quizzes(self):
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [2, 4],
                                            'quiz_category': {'type': 'Entertainment', 'id': '5'}})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 5)
        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 4)

    def test_get_quizzes_fail(self):

        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
