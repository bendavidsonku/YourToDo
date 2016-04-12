# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0012_remove_planner_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='neverEnding',
            field=models.BooleanField(default=False),
        ),
    ]
