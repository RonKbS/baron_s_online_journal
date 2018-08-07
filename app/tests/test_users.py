import json
from database.queries import db
from datetime import datetime
from app import app
from app.api import entries
import unittest


user = {'name': 'jon', 'email': 'ron@gmail.com', 'password': 'words'}
user_sign_in = {'name': 'jon', 'password': 'words'}

class TestUsers(unittest.TestCase):
    '''Run the following code before all tests'''
    def setUp(self):
        self.test_client = app.test_client()
        app.testing = True

    def tearDown(self):
        commands = (
        "DELETE FROM entries",
        "DELETE FROM users WHERE name='{}'".format('jon')
        )
        ob = db()
        cur = ob.connection.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()

    def test_signup(self):
        request = self.test_client.post('http://127.0.0.1:5000/api/v1/auth/signup',
                     data=json.dumps(user),
                     content_type='application/json')
        self.assertEqual(request.status_code, 201)
        self.assertIn(json.loads(request.data.decode()), {'201': 'User added'})