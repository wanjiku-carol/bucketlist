import unittest

from app import db, create_app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        """set up variables, environment and create tables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.user_data = {
            "username": "Yohansen",
            "email": "yohansen@testemail.com",
            "password": "test_password"
        }
        self.user_login = {"email": "yohansen@testemail.com",
                           "password": "test_password"}
        self.bucketlist = {'name': 'Adventures'}
        self.item = {
            'name': 'Rock Climbing',
            'done': 'False'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():

            db.session.remove()
            db.drop_all()
