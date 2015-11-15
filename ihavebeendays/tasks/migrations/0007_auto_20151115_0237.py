# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20150821_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='uuid',
            field=models.UUIDField(editable=False, default=uuid.uuid4),
        ),
    ]
