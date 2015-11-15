import pytest
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.utils import timezone
from ihavebeendays.core.factories import UserFactory
from ihavebeendays.tasks.forms import TaskResetForm
from ihavebeendays.tasks.models import Task, TaskReset
from ihavebeendays.tasks.views import TaskResetView


class TestTaskResetView:

    def test_response_task_reset_exists(self, response_task_reset):
        assert response_task_reset.status_code == 200

    def test_form_instance_exists_in_context(self, response_task_reset):
        assert isinstance(response_task_reset.context_data['form'], TaskResetForm)

    def test_dont_access_reset_form_from_another_user_task(self, rf, user, unfinished_task):
        unfinished_task.user = UserFactory.create(username='another-user')
        unfinished_task.save()

        request = rf.get(reverse('task-reset', kwargs={'uuid': 1}))
        request.user = user
        task_reset_view = TaskResetView.as_view()

        pytest.raises(Http404, task_reset_view, request, uuid=1)


class TestTaskResetPostView:

    @pytest.mark.django_db
    def test_reset_a_task(self, response_task_reset_post):
        tasks = Task.objects.unfinished()

        assert tasks.count() == 1
        assert tasks[0].started_at.date() == timezone.now().date()

    @pytest.mark.django_db
    def test_reset_task_create_a_taskreset_instance(self, response_task_reset_post):
        task_resets = TaskReset.objects.all()

        assert task_resets.count() == 1

    @pytest.mark.django_db
    def test_reset_task_keeps_a_description(self, response_task_reset_post):
        task_resets = TaskReset.objects.all()

        assert task_resets[0].description == 'Testing...'

    def test_redirect_to_tasks_after_reseting(self, response_task_reset_post):
        assert response_task_reset_post.status_code == 302
        assert response_task_reset_post.url == reverse('tasks')

    def test_dont_reset_tasks_from_another_user(self, rf, user, unfinished_task):
        unfinished_task.user = UserFactory.create(username='another-user')
        unfinished_task.save()

        request = rf.post(reverse('task-reset', kwargs={'uuid': 1}))
        request.user = user
        task_reset_view = TaskResetView.as_view()

        pytest.raises(Http404, task_reset_view, request, uuid=1)
