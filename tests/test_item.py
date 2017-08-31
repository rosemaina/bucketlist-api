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
        """Creates an item"""
        resp = self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)

    def test_confirm_item_creation(self):
        """Test user cannot have same buckelist items names"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        resp = self.client().post(
            '/bucketlist/1/item', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 403)
        self.assertIn('Name exists! Please choose a new one', str(resp.data))

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

    def test_api_can_get_one_item(self):
        """Test API can get one bucketlist item using it's id"""
        self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        resp = self.client().post(
            '/bucketlist/1/item/', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 201)
        id = json.loads(resp.data.decode())['id']
        result = self.client().get(
            '/bucketlist/1/item/{}'.format(id), headers=self.login())
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to disney', str(result.data))

    def test_delete_bucketlist_item(self):
        """Test API can delete a bucketlist item"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.client().post(
            '/bucketlist/1/item/', headers=self.login(), data=self.item)
        resp = self.client().delete(
            '/bucketlist/1/item/1/', headers=self.login(), data=self.item)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Bucketlist item deleted', str(resp.data))

    def test_item_search(self):
        """Test API can search for a bucketlist item"""
        self.client().post(
            '/bucketlist/', headers=self.login(), data=self.bucketlist)
        self.item['name'] = 'item100'
        self.client().post(
            '/bucketlist/1/item/', headers=self.login(), data=self.item)
        resp = self.client().get(
            '/bucketlist/1/item/?q=item100', headers=self.login())
        resp = self.client().get(
            '/bucketlist/1/item/?q=item100', headers=self.login())
        print(json.loads(resp.data.decode())['item'])
        self.assertEqual(len(json.loads(resp.data.decode())['item']), 1)

    def test_search_for_non_existent_items(self):
        """Test API can search q  for non existing data"""
        resp = self.client().get(
            '/bucketlist/1/item/?q=item100', headers=self.login(), data=self.item)
        self.assertIn('Bucketlist is non existent.Try another', str(resp.data))

    def test_get_bucketlist_items_with_limit(self):
        """Test API can search content limit"""
        self.client().post(
            '/bucketlist', headers=self.login(), data=self.bucketlist)
        self.item['name'] = 'name an item'
        self.client().post(
            '/bucketlist/1/item/', headers=self.login(), data=self.item)
        resp = self.client().get(
            '/bucketlist/1/item/?limit=1', headers=self.login(), data=self.item)
        self.assertEqual(len(json.loads(resp.data.decode())['item']), 1)

    def test_limit_is_alphanumerhic(self):
        """Test API can search content limit with aplhabets"""
        self.client().post('/bucketlist/', headers=self.login(), data=self.item)
        resp = self.client().get(
            '/bucketlist/1/item/?limit= items', headers=self.login(), data=self.item)
        self.assertIn(
            'Error, please pass a number', json.loads(resp.data.decode()).values())

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
