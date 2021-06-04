from flask_testing import TestCase
import requests_mock
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestResponse(TestBase):
    def test_index(self):
        with requests_mock.mock() as m:
            m.get('http://backend:5000/get/text', text='Some text, idk.')
            
            response = self.client.get('/')
            self.assertIn(b'Some text, idk.', response.data)