import json
import pytest
import unittest
from MyDiary import app
from mydiary.api import entries


@pytest.fixture
def client(request):
    test_client = app.test_client()
    #facilitate pushing of application context with url_for
    return test_client


def post_json(client, url, json_dict):
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')


def json_reply(reponse):
    return json.loads(reponse.data.decode('utf8'))

def test_get_all_entries(client):
    reponse = client.get('http://127.0.0.1:5000/api/v1/entries')
    assert reponse.status_code == 200