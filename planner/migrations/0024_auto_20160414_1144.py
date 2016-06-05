# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0023_auto_20160413_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringeventreference',
            name='dateOfFirstEvent',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
