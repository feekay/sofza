# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0026_auto_20160127_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='alloted',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
