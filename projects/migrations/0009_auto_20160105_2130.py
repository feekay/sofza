# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20160105_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='pay_type',
        ),
        migrations.AddField(
            model_name='project',
            name='pay_type',
            field=models.CharField(default=b'$', max_length=2, choices=[(b'$', b'Dollar'), (b'#', b'Pound'), (b'?', b'Euro')]),
        ),
    ]
