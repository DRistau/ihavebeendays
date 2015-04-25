from ibeendays.core.factories import UserFactory
from ibeendays.tasks.views import TaskListView


def test_list_my_issues(rf, tasks):
    request = rf.get('/app/')
    request.user = tasks[0].user

    task_list_view = TaskListView.as_view()
    response = task_list_view(request)

    assert len(response.context_data['task_list']) == 3


def test_cant_see_issues_from_another_user(rf, tasks):
    request = rf.get('/app/')
    request.user = tasks[0].user

    tasks[0].user = UserFactory.create(username='another-user')
    tasks[0].save()

    task_list_view = TaskListView.as_view()
    response = task_list_view(request)

    assert len(response.context_data['task_list']) == 2
