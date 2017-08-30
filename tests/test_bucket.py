"""This module holds test for the bucketlist class"""
import unittest
import os
import json
from app import db, create_app


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'email': 'test@test.com', 'password': 'testPass'}
        self.bucketlist = {'title': 'Visit America'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def registration(self):
        """Registers a user"""
        return self.client().post('/auth/register/', data=self.user)

    def login(self):
        """Logins a user"""
        self.registration()
        resp = self.client().post('/auth/login/', data=self.user)
        return {'Authorization': json.loads(resp.data.decode())['token']}

    def test_create_bucketlist(self):
        """Test API can create a bucketlist"""
        resp = self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Visit America', str(resp.data))

    def test_confirm_bucket_creation(self):
        """Test user cannot have same buckelist titles"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        resp = self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        self.assertEqual(resp.status_code, 403)
        self.assertIn('Title already taken!', str(resp.data))

    def test_blank_title(self):
        """Test that title is not blank"""
        self.bucketlist['title'] = ''
        resp = self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Blank title. Please write your title', str(resp.data))

    def test_get_all_bucketlist_when_blank(self):
        """Tests if a bucketlist exists"""
        resp = self.client().get('/bucketlist/', headers=self.login())
        self.assertEqual(resp.status_code, 404)
        self.assertIn('Bucketlists not found', str(resp.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a bucketlist using it's id"""
        resp = self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        id = json.loads(resp.data.decode())['id']
        result = self.client().get(
            '/bucketlist/{}'.format(id), headers=self.login())
        self.assertEqual(result.status_code, 200)
        self.assertIn('Visit America', str(result.data))

    def test_editing_a_bucketlist(self):
        """Test API can edit an existing bucketlist"""
        self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        self.bucketlist['title'] = 'new title'
        resp = self.client().put(
            '/bucketlist/1/', headers=self.login(), data=self.bucketlist)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('new title', str(resp.data))

    def test_delete_bucketlist(self):
        """Test API can delete a bucketlist"""
        self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        resp = self.client().delete(
            '/bucketlist/1/', headers=self.login(), data=self.bucketlist)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Bucketlist Visit America deleted', str(resp.data))
        result = self.client().get(
            '/bucketlist/1/', headers=self.login())
        self.assertEqual(result.status_code, 403)
        self.assertIn('Bucketlist Not found', str(result.data))

    def test_bucketlist_search(self):
        """Test API can serach for a bucketlist"""
        self.bucketlist['title'] = 'bucket two'
        self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        resp = self.client().get(
            '/bucketlist?q=bucket two', headers=self.login())
        self.assertIn('bucket two', str(resp.data))
        resp = self.client().get('/bucketlist?q=buck', headers=self.login())
        self.assertEqual(len(json.loads(resp.data.decode())['bucketlist']), 1)

    def test_bucketlist_search_for_non_existent(self):
        """Test API can search q  for non existing data"""
        resp = self.client().get(
            '/bucketlist?q=bucket5', headers=self.login(), data=self.bucketlist)
        self.assertIn('Bucketlists not found', str(resp.data))

    def test_get_bucketlists_with_limit(self):
        """Test API can search content limit"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.bucketlist['title'] = 'title something'
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        resp = self.client().get(
            '/bucketlist?limit=1', headers=self.login(), data=self.bucketlist)
        self.assertEqual(len(json.loads(resp.data.decode())['bucketlist']), 1)

    def test_limit_is_alphanumerhic(self):
        """Test API can search content limit with aplhabets"""
        resp = self.client().get(
            '/bucketlist?limit=test', headers=self.login(), data=self.bucketlist)
        self.assertIn(
            'Error, pass a number', json.loads(resp.data.decode()).values())

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
