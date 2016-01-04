# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20160102_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone', null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='title',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
