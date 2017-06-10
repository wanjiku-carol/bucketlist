import unittest
from flask import json
from base_test_case import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """This class represents the bucketlist test case"""

    def register_user_and_bucketlist(self):
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)
        # obtain access token
        access_token = json.loads(result.data.decode())['access_token']
        self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data=self.bucketlist)

    def test_create_item(self):
        """Test API can create a bucketlist item with a POST request"""
        self.client.post('/auth/register/', data=self.user_data)
        result = self.client.post('/auth/login/', data=self.user_data)
        # obtain access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client.post(
            '/bucketlists/',
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        bucket_id = json.loads(res.data.decode())
        # res = self.register_user_and_bucketlist()

        resp_item = self.client.post(
            'bucketlists/{}/items/'.format(bucket_id['id']),
            data=self.item)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(resp_item.status_code, 200)
        self.assertIn('Rock Climbing', str(resp_item.data))

    def test_get_all_items(self):
        """Test API can get a bucketlist items with GET request"""
        self.register_user_and_bucketlist()
        resp_item = self.client.post('/bucketlistitem/', data=self.item)
        self.assertEqual(resp_item.status_code, 201)

        res = self.client.get('/bucketlistitem/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Rock Climbing', str(resp_item.data))

    def test_get_item_by_id(self):
        """Test API can get one bucketlist using it's id."""
        self.register_user_and_bucketlist()
        resp_item = self.client.post('/bucketlistitem/', data=self.item)
        self.assertEqual(resp_item.status_code, 201)
        result_in_json = json.loads(resp_item.data)
        result = self.client.get(
            '/bucketlistitem/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Rock Climbing', str(result.data))

    def test_edit_item(self):
        """Test API can edit an existing bucketlist with PUT request"""
        self.register_user_and_bucketlist()
        resp_item = self.client.post('/bucketlistitem/', data=self.item)
        self.assertEqual(resp_item.status_code, 201)
        self.assertIn('Rock Climbing', str(resp_item.data))
        results = resp_item.data.decode()
        res = self.client.put(
            '/bucketlistitem/{}'.format(results['id']),
            data={
                "name": "Bunjee jumping without socks"
            })

        self.assertEqual(res.status_code, 200)
        self.assertIn('Bunjee jumping without socks', str(res.data))

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
        # import pdb
        # pdb.set_trace()
        resp = self.client.delete('/bucketlists/{}'.format(results['id']),
                                  headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 200)
        import pdb
        response = self.client.get('/bucketlists/{}'.format(results['id']),
                                   headers=dict(Authorization=access_token))
        # pdb.set_trace()
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
