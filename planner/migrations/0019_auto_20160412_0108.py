# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0018_auto_20160412_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringeventreference',
            name='dateOfFirstEvent',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
    ]
