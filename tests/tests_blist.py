import unittest
from flask import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.bucketlist = {'name': 'Rock Climbing'}
        self.user_data = {
            'username': 'mango',
            'email': 'mango@email.com',
            'password': 'mango_123'
        }
        with self.app.app_context():
            db.create_all()

    def test_bucketlist_create(self):
        """Test API can create a bucketlist with a POST request"""
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)
        # obtain access token
        access_token = json.loads(result.data.decode())['access_token']

        resp = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Rock Climbing', str(resp.data))

    def test_bucketlists_get_all(self):
        """Test API can get a bucketlist with GET request"""
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']

        resp = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get(
            '/bucketlists/',
            headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Rock Climbing', str(resp.data))

    def test_bucketlist_get_by_id(self):
        """Test API can get one bucketlist using it's id."""
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)

        access_token = json.loads(result.data.decode())['access_token']

        resp = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        result_in_json = json.loads(resp.data)
        result = self.client.get(
            '/bucketlists/{}'.format(result_in_json['id']),
            headers=dict(Authorization=access_token))

        self.assertEqual(result.status_code, 200)
        self.assertIn('Rock Climbing', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist with PUT request"""
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data={'name': 'Bunjee jumping'})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client.put(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization=access_token),
            data={
                "name": "Bunjee jumping without socks"
            })

        self.assertEqual(res.status_code, 200)
        # import pdb
        # pdb.set_trace()
        results = self.client.get(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization=access_token))
        self.assertIn('Bunjee jumping without socks', str(results.data))

    def test_bucketlist_delete(self):
        """Test API can delete an existing bucketlist with DELETE request"""
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)

        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        resp = self.client.delete('/bucketlists/{}'.format(results['id']),
                                  headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 200)
        result = self.client.get('/bucketlists/{}'.format(results['id']),
                                 headers=dict(Authorization=access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():

            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
