import pytest
from datetime import datetime
from core.factories import UserFactory
from tasks.factories import TaskFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def task(db):
    return TaskFactory.create()


@pytest.fixture
def unfinished_tasks(db):
    return TaskFactory.create_batch(1)


@pytest.fixture
def finished_tasks(db):
    return TaskFactory.create_batch(3, finished_at=datetime.now())


@pytest.fixture
def logged_in_request(client, user):
    client.login(username='test', password='test')

    def lazy(url):
        return client.get(url)

    return lazy
