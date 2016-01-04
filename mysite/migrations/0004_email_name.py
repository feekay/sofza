# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20160102_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
