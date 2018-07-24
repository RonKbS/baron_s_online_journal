import json
import pytest
import unittest
from datetime import datetime
from MyDiary import app
from MyDiary.api import entries


@pytest.fixture
def client(request):
    test_client = app.test_client()
    return test_client


def post_json(client, url, json_dict):
    return client.post(url, data=json.dumps(json_dict),
                       content_type='application/json')


def json_reply(reponse):
    return json.loads(reponse.data.decode('utf8'))


def test_get_all_entries(client):
    reponse = client.get('http://127.0.0.1:5000/api/v1/entries')
    assert reponse.status_code == 200


def test_add_entry(client):
    response = post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
                        {"content": 'New content added'})
    assert response.status_code == 201
    assert json_reply(response) == {"201": 'Entry added'}


def test_get_entry(client):
    '''Create entry that has an id of one, changing previous content id to 2'''
    post_response = post_json(client, 'http://127.0.0.1:5000/api/v1/entries', 
             {"content": 'More content added'})
    id = 1
    get_response = client.get('http://127.0.0.1:5000/api/v1/entries/' + str(id))
    assert post_response.status_code == 201
    assert get_response.status_code == 200



def test_delete_entry(client):
    post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
             {"content": 'New content to be deleted'})
    '''Following test to get entry, this is the second entry added hence the id of two'''
    id = 1
    response = client.delete('http://127.0.0.1:5000/api/v1/entries/' + str(id))
    assert response.status_code == 200
    assert json_reply(response) == {"200": 'Entry deleted'}