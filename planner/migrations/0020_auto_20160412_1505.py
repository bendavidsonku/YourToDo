# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0019_auto_20160412_0108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='neverEnding',
        ),
        migrations.AddField(
            model_name='recurringeventreference',
            name='neverEnding',
            field=models.BooleanField(default=False),
        ),
    ]
