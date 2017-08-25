# """This module holds test for the buxketlist class"""
# import unittest
# import os
# import json
# from app import db, create_app


# class BucketlistTestCase(unittest.TestCase):
#     """This class represents the bucketlist test case"""
#     def setUp(self):
#         """Define test variables and initialize app."""
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client
#         self.bucketlist = {'title': 'To go to Sagana'}

#         # binds the app to the current context
#         with self.app.app_context():
#             # create all tables
#             db.create_all()


#     def test_bucketlist_creation(self):
#         """Test API can create a bucketlist (POST request)"""
#         resp = self.client().post('/bucketlist', data=self.bucketlist)
#         self.assertEqual(resp.status_code, 201)
#         self.assertIn('To go to Sagana', str(resp.data))

# if __name__ == "__main__":
#     unittest.main()
