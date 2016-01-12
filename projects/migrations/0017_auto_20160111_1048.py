# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0016_staff_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='frm',
            field=models.ForeignKey(related_name='sender', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='to',
            field=models.ManyToManyField(related_name='reciever', to=settings.AUTH_USER_MODEL),
        ),
    ]
