import json
import pytest
import unittest
import psycopg2
from testing_database import config
from testing_database.create_tables import create_tables
import testing.postgresql
from datetime import datetime
from mydiary import app
from mydiary.api import entries


user = {'name': 'jon', 'email': 'ron@gmail.com', 'password': 'words'}
user_sign_in = {'name': 'jon', 'password': 'words'}
entry ={'content': 'words words'}

def post_json(client, url, json_dict):
    return client.post(url, data = json.dumps(json_dict), 
                        headers=sample_login(client), 
                        content_type='application/json')

def json_reply(reponse):
    return json.loads(reponse.data.decode())

@pytest.fixture
def client(request):
    # with testing.postgresql.Postgresql() as postgresql:
        # db = psycopg2.connect(**postgresql.dsn(host='localhost', database='testdb',
            # user='postgres', password='lefty3064'))
    test_client = app.test_client()

    test_client.post('http://127.0.0.1:5000/api/v1/auth/signup', data=json.dumps(user),
                     content_type='application/json')


    yield test_client

    commands = (
        "DELETE FROM entries WHERE entry_id='{}'".format(1),
        "DELETE FROM users WHERE name='{}'".format('jon')
        )
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    conn.close() 


def test_login(client):
    user = client.post('http://127.0.0.1:5000/api/v1/login',
                     data=json.dumps(user_sign_in), content_type='application/json')
    assert user.status_code == 200


'''Generate token to pass'''
def sample_login(client):
    response = client.post('http://127.0.0.1:5000/api/v1/login',
                     data=json.dumps(user_sign_in), content_type='application/json')
    gets = json.loads(response.data.decode('utf-8'))
    return gets

def test_get_all_entries(client):
    reply = client.get('/api/v1/entries', headers=sample_login(client))
    # import pdb; pdb.set_trace()
    assert reply.status_code == 200


def test_add_entry(client):
    response = post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
                        {"content": 'New content added'})
    assert response.status_code == 201
    assert json_reply(response) == {"201": 'Entry added'}
    # client.delete('http://127.0.0.1:5000/api/v1/entries/1')


# def test_get_entry(client):
#     '''Create entry that has an id of one, changing previous content id to 2'''
#     post_response = post_json(client, 'http://127.0.0.1:5000/api/v1/entries', 
#              {"content": 'More content added'})
#     id = 1
#     get_response = client.get('http://127.0.0.1:5000/api/v1/entries/' + str(id))
#     assert post_response.status_code == 201
#     assert get_response.status_code == 200
#     client.delete('http://127.0.0.1:5000/api/v1/entries/1')


# def test_modifiy_entry(client):
#     post_json(client, 'http://127.0.0.1:5000/api/v1/entries', 
#              {"content": ' content to be modified'})
#     response_to_change = client.put('http://127.0.0.1:5000/api/v1/entries/1', data=
#                                     json.dumps({"content": 'content modified'}), 
#                                     content_type = 'application/json')
#     assert response_to_change.status_code == 201


# def test_delete_entry(client):
#     post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
#              {"content": 'New content to be deleted'})
#     '''Following test to get entry, this is the second entry added hence the id of two'''
#     id = 1
#     response = client.delete('http://127.0.0.1:5000/api/v1/entries/' + str(id))
#     assert response.status_code == 200
#     assert json_reply(response) == {"200": 'Entry deleted'}
if __name__ == '__main__':
    create_tables()