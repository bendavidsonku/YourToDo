# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='planner',
            name='view',
            field=models.IntegerField(default=2, choices=[(1, 'Day View'), (2, 'Week View'), (3, 'Calendar View')]),
        ),
    ]
