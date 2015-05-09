from pyquery import PyQuery as pq
from django.core.urlresolvers import reverse


def test_tasks_page_as_anonymous_user_redirects_to_login(client):
    response = client.get(reverse('tasks'))

    assert response.status_code == 302
    assert response.url == 'http://testserver/login/?next=/tasks/'


def test_tasks_page_is_available_when_logged_in(logged_in_request, user):
    response = logged_in_request(reverse('tasks'))
    assert response.status_code == 200


def test_tasks_page_shows_done_and_reset_actions_when_a_task_is_already_started(logged_in_request, unfinished_tasks):
    response = logged_in_request(reverse('tasks'))
    buttons = pq(response.content).find('.cover-buttons')

    assert buttons.find('.button')[0].text == 'Reset'
    assert buttons.find('.button')[1].text == 'Done'


def test_tasks_page_shows_start_action_when_doesnt_exist_a_started_task(logged_in_request, finished_tasks):
    response = logged_in_request(reverse('tasks'))
    buttons = pq(response.content).find('.cover-buttons')

    assert buttons.find('.button')[0].text == 'Start'


def test_tasks_finished_are_listed(logged_in_request, finished_tasks):
    response = logged_in_request(reverse('tasks'))
    tasks = pq(response.content).find('.tasks-done-task')

    assert tasks.length == 3


def test_tasks_are_listed_with_titles_days_and_the_range_of_dates(logged_in_request, finished_tasks):
    response = logged_in_request(reverse('tasks'))
    task = pq(response.content).find('.tasks-done-task:eq(0)')

    assert task.find('.tasks-done-label').text() == 'Task 13'
    assert task.find('.tasks-done-days').text() == '1 day(s)'
    assert task.find('.tasks-done-dates').text() == 'Feb, 09 2015 - Feb, 10 2015'


def test_shows_a_message_when_user_doesnt_have_tasks(logged_in_request):
    response = logged_in_request(reverse('tasks'))
    tasks = pq(response.content).find('.tasks-done-empty')

    assert tasks.length
