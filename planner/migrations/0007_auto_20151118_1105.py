# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20151118_0038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='timeFrame',
            new_name='timeStart',
        ),
        migrations.AddField(
            model_name='event',
            name='timeEnd',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='timeEstimate',
            field=models.IntegerField(choices=[(1, '--'), (2, '15 minutes'), (3, '30 minutes'), (4, '45 minutes'), (5, '1 hour'), (6, '2 hours'), (7, '3 hours'), (8, '4 hours'), (9, '5 hours'), (10, '6 hours'), (11, '7 hours'), (12, '8 hours'), (13, 'More than 8 hours')], default=1),
        ),
    ]
