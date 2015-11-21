# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0009_category_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='day',
            field=models.IntegerField(choices=[(1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'Saturday')], default=1),
        ),
    ]
