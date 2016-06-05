# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20151201_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilePicture',
            field=models.ImageField(upload_to='profile-pictures', null=True),
        ),
    ]
