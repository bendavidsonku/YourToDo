# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0025_auto_20160414_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringeventreference',
            name='dateOfFirstEvent',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
