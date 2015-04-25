from django.core.urlresolvers import reverse
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.views import TaskListView


class TestTasksPage:

    def test_tasks_page_as_anonymous_user_redirects_to_login(self, client):
        response = client.get(reverse('tasks'))

        assert response.status_code == 302
        assert response.url == 'http://testserver/login/?next=/tasks/'

    def test_tasks_page_is_available_when_logged_in(self, logged_in_request, user):
        response = logged_in_request(reverse('tasks'))
        assert response.status_code == 200

    def test_tasks_page_uses_task_list_template(self, logged_in_request):
        response = logged_in_request(reverse('tasks'))
        assert 'Without sleep' in str(response.content)


def test_list_my_issues(rf, tasks):
    request = rf.get('/app/')
    request.user = tasks[0].user

    task_list_view = TaskListView.as_view()
    response = task_list_view(request)

    assert len(response.context_data['task_list']) == 3


def test_cant_see_issues_from_another_user(rf, tasks):
    request = rf.get('/app/')
    request.user = tasks[0].user

    tasks[0].user = UserFactory.create(username='another-user')
    tasks[0].save()

    task_list_view = TaskListView.as_view()
    response = task_list_view(request)

    assert len(response.context_data['task_list']) == 2
