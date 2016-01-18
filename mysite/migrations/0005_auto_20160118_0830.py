# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_email_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='details',
            field=models.CharField(default='No details', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
