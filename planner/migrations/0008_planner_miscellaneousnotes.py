# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_auto_20151118_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='planner',
            name='miscellaneousNotes',
            field=models.TextField(null=True, verbose_name='Miscellaneous'),
        ),
    ]
