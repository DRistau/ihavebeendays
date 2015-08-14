import pytest
from django.core.urlresolvers import reverse


@pytest.fixture
def login_request(client):
    return client.get(reverse('login'))


def test_login_page_is_available(login_request):
    assert login_request.status_code == 200
