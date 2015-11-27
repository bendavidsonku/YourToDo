# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0011_auto_20151122_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planner',
            name='view',
        ),
    ]
