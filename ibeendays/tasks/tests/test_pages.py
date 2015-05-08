from pyquery import PyQuery as pq
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


def test_tasks_page_shows_done_and_reset_actions_when_a_task_is_already_started(logged_in_request, unfinished_tasks):
    response = logged_in_request(reverse('tasks'))
    buttons = pq(response.content).find('.cover-buttons')

    assert buttons.find('.button')[0].text == 'Reset'
    assert buttons.find('.button')[1].text == 'Done'


def test_tasks_page_shows_start_action_when_doesnt_exist_a_started_task(logged_in_request, finished_tasks):
    response = logged_in_request(reverse('tasks'))
    buttons = pq(response.content).find('.cover-buttons')

    assert buttons.find('.button')[0].text == 'Start'
