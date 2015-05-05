import pytest
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.models import Task
from ibeendays.tasks.views import TaskCreateView, TaskListView


class TestTaskListView:

    def test_list_my_issues(self, rf, tasks):
        request = rf.get('/app/')
        request.user = tasks[0].user

        task_list_view = TaskListView.as_view()
        response = task_list_view(request)

        assert len(response.context_data['task_list']) == 3

    def test_cant_see_issues_from_another_user(self, rf, tasks):
        request = rf.get('/app/')
        request.user = tasks[0].user

        tasks[0].user = UserFactory.create(username='another-user')
        tasks[0].save()

        task_list_view = TaskListView.as_view()
        response = task_list_view(request)

        assert len(response.context_data['task_list']) == 2


class TestTaskCreateView:

    @pytest.mark.django_db
    def test_create_a_task_to_work_with(self, rf, user):
        request = rf.post('/tasks/add/', {
            'title': 'Task test',
        })
        request.user = user

        task_create_view = TaskCreateView.as_view()
        response = task_create_view(request)

        assert Task.objects.count() == 1
        assert response.status_code == 302
