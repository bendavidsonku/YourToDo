# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_category_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='Description', max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='important',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='Name', max_length=60),
        ),
        migrations.AddField(
            model_name='event',
            name='timeEstimate',
            field=models.IntegerField(default=13, choices=[(1, '15 minutes'), (2, '30 minutes'), (3, '45 minutes'), (4, '1 hour'), (5, '2 hours'), (6, '3 hours'), (7, '4 hours'), (8, '5 hours'), (9, '6 hours'), (10, '7 hours'), (11, '8 hours'), (12, 'More than 8 hours'), (13, '--')]),
        ),
        migrations.AddField(
            model_name='event',
            name='timeFrame',
            field=models.TimeField(null=True),
        ),
    ]
