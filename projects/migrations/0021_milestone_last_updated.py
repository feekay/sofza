# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20160115_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
