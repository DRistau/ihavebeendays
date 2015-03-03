from django.core.urlresolvers import reverse


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
