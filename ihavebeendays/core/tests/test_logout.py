import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def logout_request(client):
    def lazy():
        return client.get('/logout/')

    return lazy


def test_logout_redirect_to_home(logout_request):
    response = logout_request()

    assert response.status_code == 302
    assert response.url == 'http://testserver/'


def test_user_is_no_longer_authenticated_after_logout(client, logout_request, user):
    client.login(username='test', password='test')
    response = logout_request()

    assert response.wsgi_request.user.is_authenticated() is False
