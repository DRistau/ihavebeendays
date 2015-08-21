# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_data_migration_for_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='uuid',
            field=uuidfield.fields.UUIDField(max_length=32, blank=True, unique=True, editable=False, default=None),
            preserve_default=True,
        ),
    ]
