from flaskblog import app, db
import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskblog.models import User, Post

class Flask_home(unittest.TestCase):

	def setUp(self):
		app.config['TESTING']=True
		app.config['WTF_CSRF_ENABLED']=False

		
	def test_home_route(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type ='html/text')
		self.assertEqual(response.status_code, 200)

	def test_home(self):
		tester = app.test_client(self)
		response = tester.post('/login', data=dict(email="luffy@gmail.com", password="123456"), follow_redirects=True)
		self.assertIn(b"Login Successfull !!", response.data)

	def test_register_route(self):
		tester = app.test_client(self)
		response = tester.get('/register', content_type = 'html/text')
		self.assertEqual(response.status_code, 200)

	# def test_register(self):
	# 	tester = app.test_client(self)
	# 	response = tester.post('/register', data=dict(username="new1user", email="new1user@gmail.com", password="123456", confirm_password="123456"), follow_redirects=True)
	# 	self.assertIn(b"Your account has been created! You are now able to log in", response.data)

	def test_reset_route(self):
		tester = app.test_client(self)
		response = tester.get('/reset_password', content_type='html/text')
		self.assertEqual(response.status_code, 200)


	def test_reset_token(self):
		tester = app.test_client(self)
		response = tester.post('/reset_password', data=dict(email="akhil.gandhi10.ag@gmail.com"), follow_redirects=True)
		self.assertIn(b"An email has been sent for password reset", response.data)


	def test_post_id(self):
		tester = app.test_client(self)
		response = tester.get('/post/4', content_type='html/text')
		self.assertIn(b"Computer", response.data)

if __name__ == '__main__':
	unittest.main()