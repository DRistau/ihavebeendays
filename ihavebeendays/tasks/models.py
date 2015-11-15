import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class TaskQuerySet(models.QuerySet):

    def finished(self):
        return self.filter(finished_at__isnull=False).order_by('-finished_at')

    def unfinished(self):
        return self.filter(finished_at__isnull=True)


class Task(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(blank=True, null=True)
    last_longer_duration = models.IntegerField(default=0)

    objects = TaskQuerySet.as_manager()

    def __str__(self):
        return self.title

    def duration(self):
        started_at = self.started_at
        finished_at = self.finished_at

        if not finished_at:
            finished_at = timezone.now()

        delta = self._delta_between_dates(finished_at, started_at)
        return delta.days

    def longest_duration(self):
        if self.duration() > self.last_longer_duration:
            return self.duration()

        return self.last_longer_duration

    def reset(self):
        now = timezone.now()
        delta = self._delta_between_dates(now, self.started_at)

        if self.has_a_new_record(delta.days):
            self.last_longer_duration = delta.days

        self.started_at = now
        self.save()

    def done(self):
        now = timezone.now()
        delta = self._delta_between_dates(now, self.started_at)

        if self.has_a_new_record(delta.days):
            self.last_longer_duration = delta.days

        self.finished_at = now
        self.save()

    def has_a_new_record(self, duration):
        return duration > self.last_longer_duration

    def _delta_between_dates(self, date1, date2):
        return date1.date() - date2.date()


class TaskReset(models.Model):
    task = models.ForeignKey(Task)
    description = models.TextField(blank=True, null=True)
