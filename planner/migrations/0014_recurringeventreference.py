# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0013_event_neverending'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringEventReference',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('listOfDaysToOccur', models.TextField(max_length=7)),
            ],
        ),
    ]
