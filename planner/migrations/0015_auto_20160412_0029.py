# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0014_recurringeventreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringeventreference',
            name='periodOfRecurrence',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recurringeventreference',
            name='recurrenceType',
            field=models.IntegerField(default=0),
        ),
    ]
