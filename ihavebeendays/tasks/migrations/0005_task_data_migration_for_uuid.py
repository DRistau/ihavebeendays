# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models, migrations


def generate_uuid_for_already_created_tasks(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    for task in Task.objects.all():
        task.uuid = uuid.uuid1()
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_uuid'),
    ]

    operations = [
        migrations.RunPython(generate_uuid_for_already_created_tasks),
    ]
