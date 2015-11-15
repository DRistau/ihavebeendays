# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_data_migration_for_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='uuid',
            field=models.UUIDField(
                default=None,
                blank=True,
                unique=True,
                editable=False,
            ),
            preserve_default=True,
        ),
    ]
