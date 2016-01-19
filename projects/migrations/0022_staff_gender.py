# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_milestone_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='gender',
            field=models.CharField(default='m', max_length=2, choices=[(b'm', b'Male'), (b'f', b'Female')]),
            preserve_default=False,
        ),
    ]
