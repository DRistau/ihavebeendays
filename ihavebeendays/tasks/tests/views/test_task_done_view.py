import pytest
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.utils import timezone
from ihavebeendays.core.factories import UserFactory
from ihavebeendays.tasks.models import Task
from ihavebeendays.tasks.views import TaskDoneView


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
