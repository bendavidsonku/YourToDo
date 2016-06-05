# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0015_auto_20160412_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringeventreference',
            name='nthOccurenceOfSelectedDateAsInt',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='recurringeventreference',
            name='sameDayOrSameDayOfWeek',
            field=models.BooleanField(default=True),
        ),
    ]
