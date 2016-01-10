# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20160109_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='important',
            field=models.BooleanField(default=False),
        ),
    ]
