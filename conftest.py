import pytest
from core.factories import UserFactory


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def logged_in_request(client, user):
    client.login(username='test', password='test')

    def lazy(url):
        return client.get(url)

    return lazy
