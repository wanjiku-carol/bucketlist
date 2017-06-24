import unittest
from flask import json
from base_test_case import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """This class represents the bucketlist test case"""

    def test_create_bucketlist(self):
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
        self.assertIn('Adventures', str(resp.data))

    def test_get_all_bucketlists(self):
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
        self.assertIn('Adventures', str(resp.data))

    def test_get_buckelist_by_id(self):
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
        self.assertIn('Adventures', str(result.data))

    def test_edit_bucketlist(self):
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
                "name": "Cooking"
            })

        self.assertEqual(res.status_code, 200)
        results = self.client.get(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization=access_token))
        self.assertIn('Cooking', str(results.data))

    def test_delete_bucketlist(self):
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
        # import pdb
        # pdb.set_trace()
        resp = self.client.delete('/bucketlists/{}'.format(results['id']),
                                  headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 200)
        response = self.client.get('/bucketlists/{}'.format(results['id']),
                                   headers=dict(Authorization=access_token))
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
