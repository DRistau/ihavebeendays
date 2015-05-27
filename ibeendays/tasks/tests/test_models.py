from django.utils import timezone


def test_task_has_str_representation(task):
    assert str(task) == 'Factored Task'


def test_task_computes_days_between_started_at_and_finished_at(task):
    assert task.duration() == 3


def test_task_without_finished_date_returns_duration_as_zero(task):
    task.started_at = timezone.now()
    task.finished_at = None

    assert task.duration() == 0


def test_bring_only_finished_tasks(finished_tasks):
    assert len(finished_tasks) == 3


def test_bring_only_unfinished_tasks(unfinished_tasks):
    assert len(unfinished_tasks) == 1


def test_reset_task(task):
    task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
    task.reset()

    assert task.started_at.date() == timezone.now().date()


def test_done_task(task):
    task.finished_at = None
    task.done()

    assert task.finished_at.date() == timezone.now().date()


def test_task_record(task):
    task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
    task.finished_at = timezone.datetime(2015, 1, 2, 12, 0, 0)

    assert task.longest_streak() == 1
