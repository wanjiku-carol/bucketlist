import unittest
from flask import json
from base_test_case import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """This class represents the bucketlist test case"""

    def test_create_item(self):
        """Test API can create a bucketlist item with a POST request"""
        self.client.post('/auth/register/',
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(self.user_data))
        result = self.client.post('/auth/login/',
                                  headers={'Content-Type': 'application/json'},
                                  data=json.dumps(self.user_data))
        # obtain access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps(self.bucketlist))
        bucket_id = json.loads(res.data.decode())
        resp_item = self.client.post(
            'bucketlists/{}/items/'.format(bucket_id['id']),
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps(self.item))
        self.assertEqual(resp_item.status_code, 201)
        self.assertIn('Rock Climbing', str(resp_item.data))

    def test_get_item_by_id(self):
        self.client.post('/auth/register/',
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(self.user_data))
        result = self.client.post('/auth/login/',
                                  headers={'Content-Type': 'application/json'},
                                  data=json.dumps(self.user_data))
        # obtain access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps(self.bucketlist))
        bucket_id = json.loads(res.data.decode())
        resp_item = self.client.post(
            'bucketlists/{}/items/'.format(bucket_id['id']),
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps(self.item))
        self.assertEqual(resp_item.status_code, 201)
        result = json.loads(resp_item.data.decode())
        results = self.client.get(
            'bucketlists/{}/items/{}/'.format(bucket_id['id'], result['id']),
            headers=dict(Authorization=access_token))
        self.assertEqual(results.status_code, 200)

    def test_edit_item(self):
        """Test API can edit an existing bucketlist with PUT request"""
        self.client.post('/auth/register/',
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(self.user_data))
        result = self.client.post('/auth/login/',
                                  headers={'Content-Type': 'application/json'},
                                  data=json.dumps(self.user_data))
        # obtain access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps(self.bucketlist))
        bucket_id = json.loads(res.data.decode())
        resp_item = self.client.post(
            'bucketlists/{}/items/'.format(bucket_id['id']),
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps(self.item))
        self.assertEqual(resp_item.status_code, 201)
        result = json.loads(resp_item.data.decode())
        results = self.client.put(
            'bucketlists/{}/items/{}/'.format(bucket_id['id'], result['id']),
            headers={'Authorization': access_token,
                     'Content-Type': 'application/json'},
            data=json.dumps({'name': 'Water rafting', 'done': 'True'
                             }))
        self.assertEqual(results.status_code, 201)


#
#
if __name__ == "__main__":
    unittest.main()
