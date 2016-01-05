# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_milestone_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]
