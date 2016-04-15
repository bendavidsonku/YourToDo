# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0027_auto_20160414_1243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='recurringReference',
            new_name='recurrenceReference',
        ),
    ]
