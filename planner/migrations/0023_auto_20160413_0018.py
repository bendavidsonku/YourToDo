# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0022_event_neverending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurringeventreference',
            name='neverEnding',
        ),
        migrations.RemoveField(
            model_name='recurringeventreference',
            name='parentPlanner',
        ),
    ]
