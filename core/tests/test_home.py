import pytest
from django.core.urlresolvers import reverse


@pytest.fixture
def home_request(client):
    return client.get(reverse('home'))


def test_home_is_available(home_request):
    assert home_request.status_code == 200


def test_login_link_is_visible_when_user_is_anonymous(home_request):
    assert 'Log in' in str(home_request.content)
