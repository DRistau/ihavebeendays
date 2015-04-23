from django.core.urlresolvers import reverse


def test_app_view_as_anonymous_user_redirects_to_login(client):
    response = client.get(reverse('app'))

    assert response.status_code == 302
    assert response.url == 'http://testserver/login/?next=/app/'


def test_app_view_is_available_when_logged_in(logged_in_request, user):
    response = logged_in_request(reverse('app'))
    assert response.status_code == 200


def test_app_view_uses_app_template(logged_in_request):
    response = logged_in_request(reverse('app'))
    assert 'Without sleep' in str(response.content)
