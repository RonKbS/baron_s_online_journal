[![Build Status](https://travis-ci.com/RonKbS/baron_s_online_journal.svg?branch=challenge_3)](https://travis-ci.com/RonKbS/baron_s_online_journal)
[![Coverage Status](https://coveralls.io/repos/github/RonKbS/baron_s_online_journal/badge.svg?branch=challenge_3)](https://coveralls.io/github/RonKbS/baron_s_online_journal?branch=challenge_3)
[![Maintainability](https://api.codeclimate.com/v1/badges/8f742ab7eebfdcf3af26/maintainability)](https://codeclimate.com/github/RonKbS/baron_s_online_journal/maintainability)

# MyDiary

## baron_s_online_journal

The MyDiary app is one that stores your thoughts safely online. It includes html templates on the 
UI branch and a python-flask API on the api_branch

# Getting started
To run the MyDiary app on pc, create a postgres database for a postgres user and a blank password,

Then clone from the following url:
````
https://github.com/RonKbS/baron_s_online_journal.git
````

### Prerequisites

Set up a virtual environment and activate it, there after running the following from the same folder:
````
pip install -r requirements.txt
````
This will install all required packages
Note that python needs to be installed globally

### Run the app
The application is then run by:
````
set FLASK_APP=MyDiary

flask run
````
Note: Replace set with export if running linux

## Running tests

To run tests:
```
coverage run --source=MyDiary -m pytest
```

To generate an html file, viewable by checking the index.html file in htmlcov folder, run:
```
coverage html

```

## Deployment

API hosted at:
https://baron-s-mydiary.herokuapp.com/api/v1/auth/signup

## Built With

[Flask](http://flask.pocoo.org/docs/1.0/)
