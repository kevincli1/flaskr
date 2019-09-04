import pytest
from werkzeug.security import generate_password_hash
from flaskr import create_app, db
from flaskr.models import User, Post
from datetime import datetime


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    # create the database and load test data
    with app.app_context():
        db.create_all()
        user1 = User(username='test', password=generate_password_hash('test'))
        user2 = User(username='other',
                     password=generate_password_hash('other'))
        post = Post(title='test title', body=('test\nbody'),
                    author_id=1, created=datetime(2018, 1, 1))
        db.session.add_all([user1, user2, post])
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test', next=''):
        return self._client.post(
            '/auth/login' + next,
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
