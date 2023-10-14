import unittest
import json
from flask import Flask
from flask import jsonify

from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'VLib - Online Library', response.data)

    def test_get_all_books(self):
        response = self.client.get('/api/v1/books/all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_book_by_id(self):
        response = self.client.get('/api/v1/books?id=1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_book_by_invalid_id(self):
        response = self.client.get('/api/v1/books?id=100')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()