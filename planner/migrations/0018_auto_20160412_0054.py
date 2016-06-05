# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0017_event_recurringreference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recurringeventreference',
            old_name='nthOccurenceOfSelectedDateAsInt',
            new_name='nthOccurrenceOfEventDate',
        ),
        migrations.AddField(
            model_name='recurringeventreference',
            name='dateOfFirstEvent',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
