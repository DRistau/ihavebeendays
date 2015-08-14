from django.utils import timezone


class TestTaskModel:

    def test_task_has_str_representation(self, task):
        assert str(task) == 'Factored Task'

    def test_task_computes_days_between_started_at_and_finished_at(self, task):
        assert task.duration() == 3

    def test_task_without_finished_date_returns_duration_as_zero(self, task):
        task.started_at = timezone.now()
        task.finished_at = None

        assert task.duration() == 0

    def test_longest_duration(self, task):
        task.started_at = timezone.datetime(2015, 1, 1, 12, 0, 0)
        task.finished_at = timezone.datetime(2015, 1, 2, 12, 0, 0)

        assert task.longest_duration() == 1


class TestTaskReset:

    def test_reset_task(self, task):
        task.started_at = self._get_started_at()
        task.reset()

        assert task.started_at.date() == timezone.now().date()

    def test_reset_task_sets_a_longest_duration(self, task):
        task.started_at = self._get_started_at()
        task.reset()

        assert task.last_longer_duration == 3
        assert task.longest_duration() == 3

    def _get_started_at(self):
        return timezone.now() - timezone.timedelta(days=3)


class TestTaskDone:

    def test_done_task(self, task):
        task.finished_at = None
        task.done()

        assert task.finished_at.date() == timezone.now().date()

    def test_done_task_sets_a_longest_duration(self, task):
        task.started_at = self._get_started_at()
        task.done()

        assert task.last_longer_duration == 3
        assert task.longest_duration() == 3

    def _get_started_at(self):
        return timezone.now() - timezone.timedelta(days=3)


class TestTaskQuerySet:

    def test_bring_only_finished_tasks(self, finished_tasks):
        assert len(finished_tasks) == 3

    def test_bring_only_unfinished_tasks(self, unfinished_tasks):
        assert len(unfinished_tasks) == 1
