# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20150513_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='last_longer_duration',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
