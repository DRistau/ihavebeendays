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

    objects = TaskQuerySet.as_manager()

    def __str__(self):
        return self.title

    def duration(self):
        delta = self.finished_at.date() - self.started_at.date()
        return delta.days
