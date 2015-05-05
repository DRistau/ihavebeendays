import pytest
from django.core.urlresolvers import reverse
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.models import Task
from ibeendays.tasks.views import TaskCreateView, TaskListView


@pytest.fixture
def response_task_create(rf, user):
    request = rf.post('/tasks/add/', {
        'title': 'Task test',
    })
    request.user = user
    task_create_view = TaskCreateView.as_view()
    return task_create_view(request)


class TestTaskListView:

    def test_list_my_issues(self, rf, finished_tasks):
        request = rf.get('/app/')
        request.user = finished_tasks[0].user

        task_list_view = TaskListView.as_view()
        response = task_list_view(request)

        assert len(response.context_data['task_list']) == 3

    def test_cant_see_issues_from_another_user(self, rf, finished_tasks):
        request = rf.get('/app/')
        request.user = finished_tasks[0].user

        finished_tasks[0].user = UserFactory.create(username='another-user')
        finished_tasks[0].save()

        task_list_view = TaskListView.as_view()
        response = task_list_view(request)

        assert len(response.context_data['task_list']) == 2


class TestTaskCreateView:

    @pytest.mark.django_db
    def test_create_a_task_to_work_with(self, response_task_create):
        assert Task.objects.count() == 1

    def test_redirect_to_tasks_after_creation(self, response_task_create):
        assert response_task_create.status_code == 302
        assert response_task_create.url == reverse('tasks')
