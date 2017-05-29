import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Rock Climbing'}

        with self.app.app_context():
            db.create_all()

    def test_bucketlist_create(self):
        """Test API can create a bucketlist with a POST request"""
        resp = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Rock Climbing', str(resp.data))

    def test_bucketlists_get_all(self):
        """Test API can get a bucketlist with GET request"""
        resp = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/bucketlists/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Rock Climbing', str(resp.data))

    def test_bucketlist_get_by_id(self):
        """Test API can get one bucketlist using it's id."""
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Rock Climbing', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist with PUT request"""
        res = self.client().post(
            '/bucketlists/',
            data={'name': 'Bunjee jumping'})
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/bucketlists/1',
            data={
                "name": "Bunjee jumping without socks"
            })
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_delete(self):
        """Test API can delete an existing bucketlist with DELETE request"""
        res = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(res.status_code, 201)
        resp = self.client().delete('/bucketlists/1')
        self.assertEqual(resp.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():

            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
