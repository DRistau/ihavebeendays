from django.conf import settings
from django.db import models
from django.utils import timezone


class TaskQuerySet(models.QuerySet):

    def finished(self):
        return self.filter(finished_at__isnull=False)

    def unfinished(self):
        return self.filter(finished_at__isnull=True)


class Task(models.Model):
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

        delta = finished_at.date() - started_at.date()
        return delta.days

    def longest_duration(self):
        return 1

    def reset(self):
        self.started_at = timezone.now()
        self.save()

    def done(self):
        self.finished_at = timezone.now()
        self.save()
