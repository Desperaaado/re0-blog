import unittest
from flask import url_for
from app import db, app
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all() #!!
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        # db.drop_all() #!!
        self.app_context.pop()

    # def test_valid_confirmation_token(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token()
    #     self.assertTrue(u.confirm(token))

    def test_home_page(self):
        response = self.client.get(url_for('index'))
        self.assertTrue('Home' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # 注册新账户
        response = self.client.post(url_for('register'), data={
            'email': '290400112@qq.com',
            'username': 'test',
            'password': '1',
            'password2': '1'}, 
            follow_redirects=True
        )
        # self.assertTrue(response.status_code == 302)
        self.assertIn('A confirmation email has', 
                      response.get_data(as_text=True))