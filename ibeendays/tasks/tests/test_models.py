def test_task_has_str_representation(task):
    assert str(task) == 'Task 0'


def test_task_computes_days_between_started_at_and_finished_at(task):
    assert task.duration() == 3


def test_bring_only_finished_tasks(finished_tasks):
    assert len(finished_tasks) == 3


def test_bring_only_unfinished_tasks(unfinished_tasks):
    assert len(unfinished_tasks) == 1
