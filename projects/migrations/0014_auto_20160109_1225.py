# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0013_auto_20160108_0756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pay', models.IntegerField()),
                ('pay_type', models.CharField(default=b'$', max_length=2, choices=[(b'$', b'Dollar'), ('\xa3', b'Pound'), ('\u20ac', b'Euro')])),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=16)),
                ('picture', models.ImageField(upload_to=b'profile_pictures')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='success',
        ),
        migrations.AddField(
            model_name='project',
            name='completed_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='pay_type',
            field=models.CharField(default=b'$', max_length=2, choices=[(b'$', b'Dollar'), ('\xa3', b'Pound'), ('\u20ac', b'Euro')]),
        ),
        migrations.AddField(
            model_name='message',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='person',
            field=models.ForeignKey(to='projects.Staff'),
        ),
    ]
