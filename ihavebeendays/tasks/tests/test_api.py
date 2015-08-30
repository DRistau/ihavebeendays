import json
from ihavebeendays.core.factories import UserFactory


class TestTaskListApi:
    URL = '/api/v1/tasks/?format=json'

    def test_access_as_anonymous_user_shows_error(self, client, unfinished_tasks):
        response = client.get(self.URL)
        assert response.status_code == 401

    def test_access_the_list(self, logged_in_request, unfinished_tasks):
        response = logged_in_request(self.URL)
        assert response.status_code == 200

    def test_list_all_tasks_from_a_user(self, logged_in_request, finished_tasks, unfinished_tasks):
        response = logged_in_request(self.URL)
        response_as_json = json.loads(response.content.decode())

        assert len(response_as_json['objects']) == 4

    def test_dont_list_tasks_from_another_user(self, logged_in_request, unfinished_tasks):
        unfinished_tasks[0].user = UserFactory.create(username='another-user')
        unfinished_tasks[0].save()

        response = logged_in_request(self.URL)
        response_as_json = json.loads(response.content.decode())

        assert len(response_as_json['objects']) == 0


class TestTaskDetailApi:
    URL = '/api/v1/tasks/{0}/?format=json'

    def test_access_as_anonymous_user_shows_error(self, client, unfinished_tasks):
        response = self._get_from_task(client.get, unfinished_tasks[0])
        assert response.status_code == 401

    def test_access_the_details(self, logged_in_request, unfinished_tasks):
        response = self._get_from_task(logged_in_request, unfinished_tasks[0])
        assert response.status_code == 200

    def test_logged_access_shows_the_task_details(self, logged_in_request, unfinished_tasks):
        response = self._get_from_task(logged_in_request, unfinished_tasks[0])
        response_as_json = json.loads(response.content.decode())

        assert response_as_json['title'] == 'Unfinished Task'

    def test_dont_see_tasks_from_another_user(self, logged_in_request, unfinished_tasks):
        unfinished_tasks[0].user = UserFactory.create(username='another-user')
        unfinished_tasks[0].save()

        response = self._get_from_task(logged_in_request, unfinished_tasks[0])

        assert response.status_code == 401

    def _get_from_task(self, client_fn, task):
        return client_fn(self.URL.format(task.uuid))
