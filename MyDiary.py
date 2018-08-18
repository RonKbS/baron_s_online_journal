from app import app
from app.model import Diary
from app.api import entries

if __name__ == '__main__':
    app.run(ssl_context='adhoc')