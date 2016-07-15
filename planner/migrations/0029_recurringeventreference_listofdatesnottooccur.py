# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0028_auto_20160414_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringeventreference',
            name='listOfDatesNotToOccur',
            field=django.contrib.postgres.fields.ArrayField(null=True, size=None, base_field=models.DateField(default=datetime.datetime.now, null=True)),
        ),
    ]
