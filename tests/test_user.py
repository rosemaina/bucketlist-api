"""This module holds test for the user class"""
import unittest
import os
import json
from app import db, create_app


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'email': 'johndoe@email.com', 'password': '12345678'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()


    def test_user_registration(self):
        """Test API can create a user"""
        resp = self.client().post('/auth/register', data=self.user)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Successful registration!', str(resp.data))

    def test_user_exixtence(self):
        """Test API can't register a user twice"""
        user_data = {'email': 'johndoe.email@com', 'password': '12345678'}
        resp = self.client().post('/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 409)

    def test_email_validation(self):
        """Test correct email format"""
        user_data = {'email': 'johndoe,email@com', 'password': '12345678'}
        resp = self.client().post('/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 403)
        self.assertIn('Invalid email address!', str(resp.data))

    def test_password_length(self):
        """ Test confirms if password it the same'"""
        user_data = {'email': 'johndoe@email.com', 'password': '12345'}
        resp = self.client().post('/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 411)
        self.assertIn('Password length is too short!', str(resp.data))

    def test_regitration_data(self):
        """Test confirms that slots required have been filled"""
        user_data = {'email': '', 'password': ''}
        resp = self.client().post('/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Email and password required!', str(resp.data))

    def test_reset_password(self):
        """Test if password can be reset"""
        pass

    def test_user_login(self):
        """Test if user can login"""
        pass


    def test_confirm_user_login(self):
        """Test confirms that a cuser can login"""
        pass


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
