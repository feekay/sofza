# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20160103_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='cost',
        ),
        migrations.AddField(
            model_name='milestone',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='milestone',
            name='pay_type',
            field=models.CharField(default=b'$', max_length=2, choices=[(b'$', b'Dollar'), (b'#', b'Pound'), (b'?', b'Euro')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='last_updated',
            field=models.DateTimeField(),
        ),
    ]
