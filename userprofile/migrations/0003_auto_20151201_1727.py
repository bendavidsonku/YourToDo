# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20151201_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilePicture',
            field=models.ImageField(upload_to='static/media/profile-pictures', default=datetime.datetime(2015, 12, 1, 23, 27, 47, 517914, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
