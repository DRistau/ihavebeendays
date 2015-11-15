from ihavebeendays.core.factories import UserFactory
from ihavebeendays.tasks.forms import TaskForm
from ihavebeendays.tasks.views import TaskListView


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
