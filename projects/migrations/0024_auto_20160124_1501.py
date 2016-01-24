# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_auto_20160124_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='estimated_end_date',
            field=models.DateField(default=datetime.datetime(2016, 1, 24, 10, 1, 26, 468016, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 1, 24, 10, 1, 38, 589035, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
