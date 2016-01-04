# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20160103_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 1, 3, 16, 8, 42, 468973, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
