# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20160105_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='slug',
        ),
        migrations.AddField(
            model_name='milestone',
            name='success',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='milestone',
            name='url_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
        migrations.AddField(
            model_name='project',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
