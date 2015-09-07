import pytest
from pyquery import PyQuery as pq
from django.core.urlresolvers import reverse
from django.utils import timezone


@pytest.fixture
def unfinished_tasks_response(logged_in_request, unfinished_tasks):
    return logged_in_request(reverse('tasks'))


@pytest.fixture
def finished_tasks_response(logged_in_request, finished_tasks):
    finished_tasks[0].uuid = '1'
    finished_tasks[0].save()

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
        tasks = pq(finished_tasks_response.content).find('.TasksDone-task')

        assert tasks.length == 3

    def test_tasks_are_listed_with_titles_days_and_the_range_of_dates(self, finished_tasks_response):
        task = pq(finished_tasks_response.content).find('.TasksDone-task:eq(0)')

        assert 'Task' in task.find('.TasksDone-label').text()
        assert task.find('.TasksDone-days').text() == '1 day(s)'
        assert task.find('.TasksDone-dates').text() == 'Feb, 09 2015 - Feb, 10 2015'

    def test_tasks_have_a_remove_link_for_each_one(self, finished_tasks_response):
        task = pq(finished_tasks_response.content).find('.TasksDone-task:eq(0)')
        remove_url = reverse('task-delete', kwargs={
            'uuid': 1,
        })

        assert 'Remove' in task.find('.TasksDone-delete').text()
        assert task.find('.TasksDone-delete').attr('href') == remove_url

    def test_shows_a_message_when_user_doesnt_have_tasks(self, logged_in_request):
        response = logged_in_request(reverse('tasks'))
        tasks = pq(response.content).find('.TasksDone-empty')

        assert tasks.length


class TestTaskPageCover:

    def test_shows_start_action_when_doesnt_exist_a_started_task(self, finished_tasks_response):
        buttons = pq(finished_tasks_response.content).find('.Cover-buttons')

        assert buttons.find('.button')[0].value == 'Start'

    def test_shows_a_input_to_add_tasks_when_doesnt_exist_a_started_task(self, finished_tasks_response):
        input_action = pq(finished_tasks_response.content).find('.Cover-titleInputAction')

        assert input_action.length

    def test_shows_0_days_in_cover_when_doesnt_have_a_started_task(self, finished_tasks_response):
        title = pq(finished_tasks_response.content).find('.Cover-titleDays')

        assert title.text() == 'for 0 day(s)'


class TestTaskPageCoverWithUnfinishedTask:

    def test_shows_done_and_reset_actions_when_a_task_is_already_started(self, unfinished_tasks_response):
        buttons = pq(unfinished_tasks_response.content).find('.Cover-buttons')

        assert buttons.find('.button')[0].text == 'Reset'
        assert buttons.find('.button')[1].text == 'Done'

    def test_shows_task_duration_when_a_task_is_already_started(self, unfinished_tasks_response):
        title = pq(unfinished_tasks_response.content).find('.Cover-titleDays')

        assert title.text() == 'for 1 day(s)'

    def test_shows_unfinished_task_title_when_a_task_is_already_started(self, unfinished_tasks_response):
        task_title = pq(unfinished_tasks_response.content).find('.Cover-titleAction')

        assert task_title.text() == 'Unfinished Task'

    def test_shows_the_task_record_of_duration_when_task_is_already_started(self, unfinished_tasks_response):
        task_longest_duration = pq(unfinished_tasks_response.content).find('.Cover-titleLongestDuration')

        assert task_longest_duration.text() == '(Your record is 1 day(s))'

    def test_doesnt_show_the_task_longest_duration_if_it_is_zero(self, logged_in_request, unfinished_tasks):
        unfinished_tasks[0].started_at = timezone.now()
        unfinished_tasks[0].save()

        response = logged_in_request(reverse('tasks'))
        task_longest_duration = pq(response.content).find('.Cover-titleLongestDuration')

        assert len(task_longest_duration) == 0
