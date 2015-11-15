# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20151115_0237'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskReset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.TextField(null=True, blank=True)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
        ),
    ]
