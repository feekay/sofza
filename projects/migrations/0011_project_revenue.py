# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20160107_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='revenue',
            field=models.IntegerField(default=0),
        ),
    ]
