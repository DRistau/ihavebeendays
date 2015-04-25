import pytest
from ibeendays.tasks.factories import TaskFactory

pytestmark = pytest.mark.django_db


def test_task_has_str_representation():
    task = TaskFactory.create()
    assert str(task) == 'Task 0'
