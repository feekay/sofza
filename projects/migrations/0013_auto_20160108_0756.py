# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_project_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='paid',
        ),
        migrations.AddField(
            model_name='milestone',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
