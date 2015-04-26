from django.core.urlresolvers import reverse


def test_tasks_page_as_anonymous_user_redirects_to_login(client):
    response = client.get(reverse('tasks'))

    assert response.status_code == 302
    assert response.url == 'http://testserver/login/?next=/tasks/'


def test_tasks_page_is_available_when_logged_in(logged_in_request, user):
    response = logged_in_request(reverse('tasks'))
    assert response.status_code == 200


def test_tasks_page_uses_task_list_template(logged_in_request):
    response = logged_in_request(reverse('tasks'))
    assert 'Without sleep' in str(response.content)
