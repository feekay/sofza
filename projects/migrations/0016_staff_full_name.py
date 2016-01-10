# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_milestone_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='full_name',
            field=models.CharField(default='full name', max_length=50),
            preserve_default=False,
        ),
    ]
