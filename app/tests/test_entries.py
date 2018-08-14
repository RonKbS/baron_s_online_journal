import json
import pytest
import psycopg2
from database.queries import db
from datetime import datetime
from app import app
from app.api import entries


user = {'name': 'jon', 'email': 'ron@gmail.com', 'password': 'words'}
user_sign_in = {'name': 'jon', 'password': 'words'}
entry = {"title": "Title", "content": 'New content added'}
moded_entry = {"title": "Changed Title", "content": 'Modified content'}


def post_json(client, url, json_dict):
    return client.post(url, data=json.dumps(json_dict),
                       headers=sample_login(client),
                       content_type='application/json')


def json_reply(reponse):
    return json.loads(reponse.data.decode())


@pytest.fixture
def client(request):
    app.config['TESTING'] = True
    app.config['connection'] = psycopg2.connect(
            database='travis_ci_test',
            user='postgres',
            password=' ',
            host='localhost',
            port='5432')
    test_db = db()
    test_db.create_tables('users', 'entries')
    test_client = app.test_client()
    test_client.post('http://127.0.0.1:5000/api/v1/auth/signup',
                     data=json.dumps(user),
                     content_type='application/json')

    yield test_client

    commands = (
        "DROP TABLE entries",
        "DROP TABLE users"
    )
    ob = db()
    cur = ob.connection.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()


'''Generate token to pass'''
def sample_login(client):
    response = client.post(
        'http://127.0.0.1:5000/api/v1/login',
        data=json.dumps(user_sign_in),
        content_type='application/json')
    gets = json.loads(response.data.decode('utf-8'))
    return gets


def test_get_all_entries(client):
    reply = client.get('/api/v1/entries', headers=sample_login(client))
    assert reply.status_code == 200


def test_add_entry(client):
    response = post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
                         entry)
    assert response.status_code == 201
    assert json_reply(response) == {"Message": 'Entry added'}


def test_get_entry(client):
    '''Create entry that has an id of one'''
    post_entry = post_json(
        client,
        'http://127.0.0.1:5000/api/v1/entries',
        entry)
    '''get_id receives a dictionary containing a list'''
    get_entry = client.get(
        'http://127.0.0.1:5000/api/v1/entries/1',
        headers=sample_login(client))
    assert post_entry.status_code == 201
    assert get_entry.status_code == 200
    message = json_reply(get_entry)
    assert message['title'] == 'Title'


def test_modifiy_entry(client):
    post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
              entry)
    response_to_change = client.put(
        'http://127.0.0.1:5000/api/v1/entries/1',
        headers=sample_login(client),
        data=json.dumps(moded_entry),
        content_type='application/json')
    assert response_to_change.status_code == 201


def test_delete_entry(client):
    post_json(client, 'http://127.0.0.1:5000/api/v1/entries',
              entry)
    id = 1
    response = client.delete(
        'http://127.0.0.1:5000/api/v1/entries/' + str(id),
        headers=sample_login(client))
    assert response.status_code == 200
    assert json_reply(response) == {"Message": 'Entry deleted'}
