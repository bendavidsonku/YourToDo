# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0011_auto_20151120_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='day',
        ),
    ]
