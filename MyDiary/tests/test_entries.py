import unittest
import os
import json
import requests
import pytest
from flask import url_for
from mydiary import app, model
from mydiary.api import entries

@pytest.fixture
def client():
    client = MyDiary
class TestAPIEntries(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_add_entry(self):
        response = requests.post(url_for('add_entry'))
        self.assertEqual(reponse.json(), {})