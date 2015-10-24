import pytest
import json
from ihavebeendays.core.factories import UserFactory


@pytest.fixture
def another_user_task(unfinished_tasks):
    unfinished_tasks[0].user = UserFactory.create(username='another-user')
    unfinished_tasks[0].save()

    return unfinished_tasks[0]


@pytest.fixture
def response_as_json(logged_in_request):
    def lazy(url):
        response = logged_in_request(url)
        response_as_json = json.loads(response.content.decode())
        return response_as_json

    return lazy


class TestTaskListApi:
    URL = '/api/v1/tasks/?format=json'

    def test_access_as_anonymous_user_shows_error(self, client, unfinished_tasks):
        response = client.get(self.URL)
        assert response.status_code == 401

    def test_access_the_list(self, logged_in_request, unfinished_tasks):
        response = logged_in_request(self.URL)
        assert response.status_code == 200

    def test_list_all_tasks_from_a_user(self, response_as_json, finished_tasks, unfinished_tasks):
        response = response_as_json(self.URL)
        assert len(response['objects']) == 4

    def test_dont_list_tasks_from_another_user(self, response_as_json, another_user_task):
        response = response_as_json(self.URL)
        assert len(response['objects']) == 0


class TestTaskDetailApi:
    URL = '/api/v1/tasks/{0}/?format=json'

    def test_access_as_anonymous_user_shows_error(self, client, unfinished_tasks):
        response = self._get_from_task(client.get, unfinished_tasks[0])
        assert response.status_code == 401

    def test_access_the_details(self, logged_in_request, unfinished_tasks):
        response = self._get_from_task(logged_in_request, unfinished_tasks[0])
        assert response.status_code == 200

    def test_logged_access_shows_the_task_details(self, response_as_json, unfinished_tasks):
        response = self._get_from_task(response_as_json, unfinished_tasks[0])
        assert response['title'] == 'Unfinished Task'

    def test_dont_see_tasks_from_another_user(self, logged_in_request, another_user_task):
        response = self._get_from_task(logged_in_request, another_user_task)
        assert response.status_code == 401

    def _get_from_task(self, client_fn, task):
        return client_fn(self.URL.format(task.uuid))


class TestTaskSchemaApi:
    URL = '/api/v1/tasks/schema/?format=json'

    def test_access_as_anonymous_user_shows_error(self, client):
        response = client.get(self.URL)
        assert response.status_code == 401

    def test_access_the_schema(self, logged_in_request):
        response = logged_in_request(self.URL)
        assert response.status_code == 200
