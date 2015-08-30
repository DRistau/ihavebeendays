class TestTaskApi:

    def test_access_as_anonymous_user_shows_error(self, client, unfinished_tasks):
        response = client.get('/api/v1/tasks/?format=json')
        assert response.status_code == 401

    def test_access_the_task_list(self, logged_in_request, unfinished_tasks):
        response = logged_in_request('/api/v1/tasks/?format=json')
        assert response.status_code == 200
