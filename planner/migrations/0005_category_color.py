# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_planner_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.IntegerField(choices=[(1, 'Red'), (2, 'Dark Red'), (3, 'Light Red'), (4, 'Blue'), (5, 'Dark Blue'), (6, 'Light Blue'), (7, 'Green'), (8, 'Dark Green'), (9, 'Light Green'), (10, 'Yellow'), (11, 'Gold'), (12, 'Orange'), (13, 'Pink'), (14, 'Turquoise'), (15, 'Navy')], default=10),
        ),
    ]
