"""This module holds test for the bucketlist class"""
import unittest
import os
import json
from app import db, create_app


class ItemTestCase(unittest.TestCase):
    """This class represents the bucketlist item test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'email': 'test@test.com', 'password': 'testPass'}
        self.bucketlist = {'title': 'Visit America'}
        self.item = {'name': 'Go to disney'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def registration(self):
        """Registers a user"""
        return self.client().post('/auth/register', data=self.user)

    def login(self):
        """Logins a user"""
        self.registration()
        resp = self.client().post('/auth/login', data=self.user)
        return {'Authorization': json.loads(resp.data.decode())['token']}

    def test_create_bucketlist(self):
        """Creates a bucketlist"""
        resp = self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)

    def test_create_item(self):
        """Test API can create a bucketlist item"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        resp = self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Go to disney', str(resp.data))

    def test_confirm_item_creation(self):
        """Test user cannot have same buckelist items names"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        resp = self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 403)
        self.assertIn('Name already exists', str(resp.data))

    def test_blank_item_name(self):
        """Test that name is blank"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.item['name'] = ''
        resp = self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Item name not given!', str(resp.data))

    def test_editing_a_bucketlist_item(self):
        """Test API can edit an existing bucketlist item"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        self.item['name'] = 'new name'
        resp = self.client().put(
            '/bucketlist/1/item/1', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('new name', str(resp.data))

    def test_delete_bucketlist_item(self):
        """Test API can delete a bucketlist item"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        resp = self.client().delete(
            '/bucketlist/1/item/1', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Bucketlist item deleted', str(resp.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
