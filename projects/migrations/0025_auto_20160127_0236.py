# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_auto_20160124_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='estimated_end_date',
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.CharField(default=b'etc', max_length=5, choices=[(b'Fb', b'Facebook'), (b'Sk', b'Skype'), (b'Fvr', b'Fivrr'), (b'Mail', b'Mail'), (b'pph', b'P/Hour'), (b'etc', b'Others')]),
        ),
    ]
