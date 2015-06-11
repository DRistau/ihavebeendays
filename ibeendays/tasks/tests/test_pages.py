import pytest
from pyquery import PyQuery as pq
from django.core.urlresolvers import reverse


@pytest.fixture
def unfinished_tasks_response(logged_in_request, unfinished_tasks):
    return logged_in_request(reverse('tasks'))


@pytest.fixture
def finished_tasks_response(logged_in_request, finished_tasks):
    return logged_in_request(reverse('tasks'))


class TestTaskPageAccess:

    def test_access_as_anonymous_user_redirects_to_login(self, client):
        response = client.get(reverse('tasks'))

        assert response.status_code == 302
        assert response.url == 'http://testserver/login/?next=/tasks/'

    def test_page_is_available_when_logged_in(self, unfinished_tasks_response):
        assert unfinished_tasks_response.status_code == 200


class TestTaskPageList:

    def test_tasks_finished_are_listed(self, finished_tasks_response):
        tasks = pq(finished_tasks_response.content).find('.tasks-done-task')

        assert tasks.length == 3

    def test_tasks_are_listed_with_titles_days_and_the_range_of_dates(self, finished_tasks_response):
        task = pq(finished_tasks_response.content).find('.tasks-done-task:eq(0)')

        assert 'Task' in task.find('.tasks-done-label').text()
        assert task.find('.tasks-done-days').text() == '1 day(s)'
        assert task.find('.tasks-done-dates').text() == 'Feb, 09 2015 - Feb, 10 2015'

    def test_shows_a_message_when_user_doesnt_have_tasks(self, logged_in_request):
        response = logged_in_request(reverse('tasks'))
        tasks = pq(response.content).find('.tasks-done-empty')

        assert tasks.length


class TestTaskPageCover:

    def test_shows_start_action_when_doesnt_exist_a_started_task(self, finished_tasks_response):
        buttons = pq(finished_tasks_response.content).find('.cover-buttons')

        assert buttons.find('.button')[0].value == 'Start'

    def test_shows_a_input_to_add_tasks_when_doesnt_exist_a_started_task(self, finished_tasks_response):
        input_action = pq(finished_tasks_response.content).find('.cover-title-input-action')

        assert input_action.length

    def test_shows_0_days_in_cover_when_doesnt_have_a_started_task(self, finished_tasks_response):
        title = pq(finished_tasks_response.content).find('.cover-title-days')

        assert title.text() == '0 day(s)'


class TestTaskPageCoverWithUnfinishedTask:

    def test_shows_done_and_reset_actions_when_a_task_is_already_started(self, unfinished_tasks_response):
        buttons = pq(unfinished_tasks_response.content).find('.cover-buttons')

        assert buttons.find('.button')[0].text == 'Reset'
        assert buttons.find('.button')[1].text == 'Done'

    def test_shows_task_duration_when_a_task_is_already_started(self, unfinished_tasks_response):
        title = pq(unfinished_tasks_response.content).find('.cover-title-days')

        assert title.text() == '1 day(s)'

    def test_shows_unfinished_task_title_when_a_task_is_already_started(self, unfinished_tasks_response):
        task_title = pq(unfinished_tasks_response.content).find('.cover-title-action')

        assert task_title.text() == 'Unfinished Task'
