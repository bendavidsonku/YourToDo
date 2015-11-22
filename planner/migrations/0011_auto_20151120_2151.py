# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0010_event_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='dateOfEvent',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='planner',
            name='view',
            field=models.IntegerField(choices=[(1, 'Day'), (2, 'Week'), (3, 'Month')], default=2),
        ),
    ]
