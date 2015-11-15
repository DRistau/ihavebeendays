import pytest
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.utils import timezone
from django.contrib.messages.storage.fallback import FallbackStorage
from ihavebeendays.core.factories import UserFactory
from ihavebeendays.tasks.forms import TaskForm
from ihavebeendays.tasks.models import Task
from ihavebeendays.tasks.views import (TaskCreateView, TaskDeleteView,
                                       TaskDoneView, TaskListView,
                                       TaskResetView)


@pytest.fixture
def response_task_create(rf, user):
    request = rf.post(reverse('task-create'), {
        'title': 'Task test',
    })
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_create_view = TaskCreateView.as_view()
    return task_create_view(request)


@pytest.fixture
def request_finished_tasks(rf, finished_tasks):
    request = rf.get(reverse('tasks'))
    request.user = finished_tasks[0].user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    return request


@pytest.fixture
def request_unfinished_tasks(rf, unfinished_tasks):
    request = rf.get(reverse('tasks'))
    request.user = unfinished_tasks[0].user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    return request


@pytest.fixture
def unfinished_task(task):
    task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
    task.finished_at = None
    task.save()

    return task


@pytest.fixture
def response_task_reset(rf, user, unfinished_task):
    request = rf.post(reverse('task-reset', kwargs={'uuid': 1}))
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_reset_view = TaskResetView.as_view()
    return task_reset_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')


@pytest.fixture
def response_task_done(rf, user, unfinished_tasks):
    request = rf.get(reverse('task-done', kwargs={'uuid': 1}))
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_done_view = TaskDoneView.as_view()
    return task_done_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')


@pytest.fixture
def response_task_delete(rf, user, finished_tasks):
    finished_tasks[0].uuid = '7f1741b8-6cbd-4de7-b324-8840d643e08a'
    finished_tasks[0].save()

    request = rf.get(reverse('task-delete', kwargs={'uuid': '1'}))
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_delete_view = TaskDeleteView.as_view()
    return task_delete_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')


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
    def test_reset_a_task(self, response_task_reset):
        tasks = Task.objects.unfinished()

        assert tasks.count() == 1
        assert tasks[0].started_at.date() == timezone.now().date()

    def test_redirect_to_tasks_after_reseting(self, response_task_reset):
        assert response_task_reset.status_code == 302
        assert response_task_reset.url == reverse('tasks')

    def test_dont_reset_tasks_from_another_user(self, rf, user, unfinished_task):
        unfinished_task.user = UserFactory.create(username='another-user')
        unfinished_task.save()

        request = rf.get(reverse('task-reset', kwargs={'uuid': 1}))
        request.user = user
        task_reset_view = TaskResetView.as_view()

        pytest.raises(Http404, task_reset_view, request, uuid=1)


class TestTaskDoneView:

    @pytest.mark.django_db
    def test_finish_a_task(self, response_task_done):
        tasks = Task.objects.finished()

        assert tasks.count() == 1
        assert tasks[0].finished_at.date() == timezone.now().date()

    def test_redirect_to_tasks_after_finishing(self, response_task_done):
        assert response_task_done.status_code == 302
        assert response_task_done.url == reverse('tasks')

    def test_dont_finish_a_task_from_another_user(self, rf, user, unfinished_task):
        unfinished_task.user = UserFactory.create(username='another-user')
        unfinished_task.save()

        request = rf.get(reverse('task-done', kwargs={'uuid': 1}))
        request.user = user
        task_done_view = TaskDoneView.as_view()

        pytest.raises(Http404, task_done_view, request, uuid=1)


class TestTaskDeleteView:

    @pytest.mark.django_db
    def test_remove_a_task(self, response_task_delete):
        tasks = Task.objects.filter(uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')
        assert tasks.count() == 0

    def test_redirect_to_tasks_after_removing(self, response_task_delete):
        assert response_task_delete.status_code == 302
        assert response_task_delete.url == reverse('tasks')

    def test_dont_remove_an_unfinished_task(self, rf, user, unfinished_tasks):
        unfinished_tasks[0].uuid = '7f1741b8-6cbd-4de7-b324-8840d643e08a'
        unfinished_tasks[0].save()

        request = rf.get(reverse('task-delete', kwargs={'uuid': 2}))
        request.user = user
        request.session = 'session'
        request._messages = FallbackStorage(request)

        task_delete_view = TaskDeleteView.as_view()

        pytest.raises(Http404, task_delete_view, request, uuid=2)

    def test_dont_remove_a_task_from_another_user(self, rf, user, finished_tasks):
        finished_tasks[0].uuid = 1
        finished_tasks[0].user = UserFactory.create(username='another-user')
        finished_tasks[0].save()

        request = rf.get(reverse('task-delete', kwargs={'uuid': 1}))
        request.user = user
        request.session = 'session'
        request._messages = FallbackStorage(request)
        task_delete_view = TaskDeleteView.as_view()

        pytest.raises(Http404, task_delete_view, request, uuid=1)
