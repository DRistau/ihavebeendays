import pytest
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.utils import timezone
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.forms import TaskForm
from ibeendays.tasks.models import Task
from ibeendays.tasks.views import TaskCreateView, TaskListView, TaskResetView


@pytest.fixture
def response_task_create(rf, user):
    request = rf.post(reverse('task-create'), {
        'title': 'Task test',
    })
    request.user = user
    task_create_view = TaskCreateView.as_view()
    return task_create_view(request)


@pytest.fixture
def request_finished_tasks(rf, finished_tasks):
    request = rf.get(reverse('tasks'))
    request.user = finished_tasks[0].user
    return request


@pytest.fixture
def request_unfinished_tasks(rf, unfinished_tasks):
    request = rf.get(reverse('tasks'))
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


class TestTaskResetView:

    @pytest.mark.django_db
    def test_reset_a_task(self, rf, user, task):
        task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
        task.finished_at = None
        task.save()

        request = rf.get(reverse('task-reset', kwargs={'pk': 1}))
        request.user = user
        task_reset_view = TaskResetView.as_view()
        task_reset_view(request, pk=1)

        tasks = Task.objects.unfinished()

        assert tasks.count() == 1
        assert tasks[0].started_at.date() == timezone.now().date()

    def test_redirect_to_tasks_after_reseting(self, rf, user, task):
        task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
        task.finished_at = None
        task.save()

        request = rf.get(reverse('task-reset', kwargs={'pk': 1}))
        request.user = user
        task_reset_view = TaskResetView.as_view()
        response = task_reset_view(request, pk=1)

        assert response.status_code == 302
        assert response.url == reverse('tasks')

    def test_dont_reset_tasks_from_another_user(self, rf, user, task):
        task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
        task.finished_at = None
        task.user = UserFactory.create(username='another-user')
        task.save()

        request = rf.get(reverse('task-reset', kwargs={'pk': 1}))
        request.user = user
        task_reset_view = TaskResetView.as_view()

        pytest.raises(Http404, task_reset_view, request, pk=1)
