# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0020_auto_20160412_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringeventreference',
            name='parentPlanner',
            field=models.ForeignKey(default=1, to='planner.Planner'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recurringeventreference',
            name='listOfDaysToOccur',
            field=models.TextField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='recurringeventreference',
            name='sameDayOrSameDayOfWeek',
            field=models.NullBooleanField(default=True),
        ),
    ]
