# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_taskreset'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskreset',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
