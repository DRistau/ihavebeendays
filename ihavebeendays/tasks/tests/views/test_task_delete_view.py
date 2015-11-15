import pytest
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.contrib.messages.storage.fallback import FallbackStorage
from ihavebeendays.core.factories import UserFactory
from ihavebeendays.tasks.models import Task
from ihavebeendays.tasks.views import TaskDeleteView


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
