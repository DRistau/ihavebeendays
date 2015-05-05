import pytest
from datetime import datetime
from ibeendays.tasks.factories import TaskFactory
from ibeendays.tasks.models import Task


def test_task_has_str_representation(task):
    assert str(task) == 'Task 0'


@pytest.mark.django_db
def test_bring_only_finished_tasks(tasks):
    TaskFactory.create(finished_at=datetime.now())
    assert Task.objects.finished().count() == 1


def test_bring_only_unfinished_tasks(tasks):
    assert Task.objects.unfinished().count() == 3
