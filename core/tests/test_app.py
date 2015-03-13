import pytest
from django.core.urlresolvers import reverse
from core.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    return UserFactory.create()


def test_home_should_be_available(client):
    route = reverse('home')
    response = client.get(route)

    assert response.status_code == 200


def test_home_should_print_login_link_if_user_is_anonymous(client):
    route = reverse('home')
    response = client.get(route)

    assert 'Sign in' in str(response.content)


def test_login_page_should_be_available(client):
    route = reverse('login')
    response = client.get(route)

    assert response.status_code == 200


def test_logout_route_should_redirect_to_home(client):
    response = client.get('/logout/')

    assert response.status_code == 302
    assert response.url == 'http://testserver/'


def test_should_logout_the_user(client, user):
    client.login(username='test', password='test')
    response = client.get('/logout/')

    assert response.wsgi_request.user.is_authenticated() is False
