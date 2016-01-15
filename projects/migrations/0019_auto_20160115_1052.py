# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_message_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=20)),
                ('cost', models.PositiveIntegerField()),
                ('qty', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('discount', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='rating',
            field=models.DecimalField(default=5, max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='pay',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='cost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='cost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='revenue',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
        ),
        migrations.AddField(
            model_name='details',
            name='invoice',
            field=models.ForeignKey(to='projects.Invoice'),
        ),
    ]
