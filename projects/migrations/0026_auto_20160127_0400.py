# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20160127_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='source',
            field=models.CharField(default=b'etc', max_length=5, choices=[(b'fb', b'Facebook'), (b'sk', b'Skype'), (b'fvr', b'Fivrr'), (b'mail', b'Mail'), (b'pph', b'P/Hour'), (b'etc', b'Others')]),
        ),
    ]
