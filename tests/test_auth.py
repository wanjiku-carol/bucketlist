import unittest
import json

from app import db, create_app


class TestAuth(unittest.TestCase):

    def setUp(self):
        """set up variables, environment and create tables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.user_data = {
            'username': 'Yohansen',
            'email': 'yohansen@testemail.com',
            'password': 'test_password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_register_new_user(self):
        """test a new user can register"""
        res = self.client.post('/auth/register/', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You have registered successfully")
        self.assertEqual(res.status_code, 201)

    def test_user_already_exists(self):
        res = self.client.post('/auth/register/', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        # register user again
        repeat_res = self.client.post('/auth/register/', data=self.user_data)
        # check request has been accepted for processing but has not been processed
        self.assertEqual(repeat_res.status_code, 202)
        rep_result = json.loads(repeat_res.data.decode())

        self.assertEqual(rep_result['message'], "User already exists")

    def test_login_user(self):
        res = self.client.post('/auth/register/', data=self.user_data)

        self.assertEqual(res.status_code, 201)

        login_res = self.client.post('/auth/login/', data=self.user_data)

        result = json.loads(login_res.data.decode())

        self.assertEqual(result['message'], "You logged in successfully")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_login_invalid_login(self):
        wrong_user = {
            "username": "you_guy",
            "email": "you_guy@email.com",
            "password": "you_guy_password"
        }
        res = self.client.post('/auth/login/', data=wrong_user)
        result = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid email or password. Try again please.")
