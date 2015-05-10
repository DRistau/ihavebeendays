import pytest
from django.core.urlresolvers import reverse
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.forms import TaskForm
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


@pytest.fixture
def request_finished_tasks(rf, finished_tasks):
    request = rf.get('/app/')
    request.user = finished_tasks[0].user
    return request


@pytest.fixture
def request_unfinished_tasks(rf, unfinished_tasks):
    request = rf.get('/app/')
    request.user = unfinished_tasks[0].user
    return request


class TestTaskListView:

    def test_form_instance_exists_in_context(self, request_finished_tasks):
        task_list_view = TaskListView.as_view()
        response = task_list_view(request_finished_tasks)

        assert isinstance(response.context_data['task_form'], TaskForm)

    def test_list_my_finished_issues(self, request_finished_tasks):
        task_list_view = TaskListView.as_view()
        response = task_list_view(request_finished_tasks)

        assert len(response.context_data['task_list']) == 3

    def test_see_my_unfinished_issue_in_highlight(self, request_unfinished_tasks):
        task_list_view = TaskListView.as_view()
        response = task_list_view(request_unfinished_tasks)

        assert len(response.context_data['task_started']) == 1

    def test_cant_see_finished_issues_from_another_user(self, request_finished_tasks, finished_tasks):
        finished_tasks[0].user = UserFactory.create(username='another-user')
        finished_tasks[0].save()

        task_list_view = TaskListView.as_view()
        response = task_list_view(request_finished_tasks)

        assert len(response.context_data['task_list']) == 2

    def test_cant_see_unfinished_issues_from_another_user(self, request_unfinished_tasks, unfinished_tasks):
        unfinished_tasks[0].user = UserFactory.create(username='another-user')
        unfinished_tasks[0].save()

        task_list_view = TaskListView.as_view()
        response = task_list_view(request_unfinished_tasks)

        assert len(response.context_data['task_list']) == 0


class TestTaskCreateView:

    @pytest.mark.django_db
    def test_create_a_task_to_work_with(self, response_task_create):
        assert Task.objects.count() == 1

    def test_redirect_to_tasks_after_creation(self, response_task_create):
        assert response_task_create.status_code == 302
        assert response_task_create.url == reverse('tasks')
