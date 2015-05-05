from django.conf import settings
from django.db import models


class TaskQuerySet(models.QuerySet):

    def finished(self):
        return self.filter(finished_at__isnull=False)

    def unfinished(self):
        return self.filter(finished_at__isnull=True)


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    objects = TaskQuerySet.as_manager()

    def __str__(self):
        return self.title
