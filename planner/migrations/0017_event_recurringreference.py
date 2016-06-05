# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0016_auto_20160412_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='recurringReference',
            field=models.ForeignKey(null=True, to='planner.RecurringEventReference'),
        ),
    ]
