# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20160115_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='type',
            field=models.CharField(default='Developer', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='address',
            field=models.CharField(default='Karachi', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='details',
            name='desc',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='project',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
