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

    def registration(self):
        """Test API can register a user"""
        resp = self.client().post('/auth/register', data=self.user)


    def test_user_registration(self):
        """Test API can create a user"""
        resp = self.client().post('/auth/register', data=self.user)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Successful registration!', str(resp.data))

    def test_user_existence(self):
        """Test API can't register a user twice"""
        user_data = {'email': 'johndoe.email@com', 'password': '12345678'}
        resp = self.client().post('/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 403)

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

    def test_registration_data(self):
        """Test confirms that slots required have been filled"""
        user_data = {'email': '', 'password': ''}
        resp = self.client().post('/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Email and password required!', str(resp.data))

    def test_login(self):
        """Test API can login a user"""
        self.registration()
        resp = self.client().post('/auth/login', data=self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', str(resp.data))

    def test_login_with_wrong_password(self):
        """Test for wrong password"""
        self.registration()
        self.user['password'] = 'wrongPass'
        resp = self.client().post('/auth/login', data=self.user)
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Wrong password!', str(resp.data))

    def test_login_with_missing_data(self):
        """Test for wrong password"""
        self.registration()
        self.user = {'email': '', 'password': '' }
        resp = self.client().post('/auth/login', data=self.user)
        self.assertEqual(resp.status_code, 401)
        self.assertIn('User not found', str(resp.data))

    def test_logout(self):
        """Test API can logout a user"""
        resp = self.client().post('/auth/logout', data=self.user)

    def test_reset_password(self):
        """Test API can reset password for a user"""
        self.registration()
        self.user['password'] = 'test2'
        resp = self.client().post('/auth/reset-password', data=self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Password has changed successfully', str(resp.data))

        resp = self.client().post('/auth/login', data=self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', str(resp.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
