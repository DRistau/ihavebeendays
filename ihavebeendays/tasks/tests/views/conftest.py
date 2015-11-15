import pytest
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.messages.storage.fallback import FallbackStorage
from ihavebeendays.tasks.views import (TaskCreateView, TaskDeleteView,
                                       TaskDoneView, TaskResetView)


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
    request = rf.get(reverse('task-reset', kwargs={'uuid': '7f1741b8-6cbd-4de7-b324-8840d643e08a'}))
    request.user = user

    task_reset_view = TaskResetView.as_view()
    return task_reset_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')


@pytest.fixture
def response_task_reset_post(rf, user, unfinished_task):
    url = reverse('task-reset', kwargs={'uuid': '7f1741b8-6cbd-4de7-b324-8840d643e08a'})

    request = rf.post(url, {
        'description': 'Testing...',
    })
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_reset_view = TaskResetView.as_view()
    return task_reset_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')


@pytest.fixture
def response_task_done(rf, user, unfinished_tasks):
    request = rf.get(reverse('task-done', kwargs={'uuid': '7f1741b8-6cbd-4de7-b324-8840d643e08a'}))
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_done_view = TaskDoneView.as_view()
    return task_done_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')


@pytest.fixture
def response_task_delete(rf, user, finished_tasks):
    finished_tasks[0].uuid = '7f1741b8-6cbd-4de7-b324-8840d643e08a'
    finished_tasks[0].save()

    request = rf.get(reverse('task-delete', kwargs={'uuid': '7f1741b8-6cbd-4de7-b324-8840d643e08a'}))
    request.user = user
    request.session = 'session'
    request._messages = FallbackStorage(request)

    task_delete_view = TaskDeleteView.as_view()
    return task_delete_view(request, uuid='7f1741b8-6cbd-4de7-b324-8840d643e08a')
