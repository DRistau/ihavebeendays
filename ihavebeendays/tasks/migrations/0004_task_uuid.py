# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_last_longer_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='uuid',
            field=models.UUIDField(max_length=32, blank=True, null=True, editable=False),
            preserve_default=True,
        ),
    ]
