# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=60)),
                ('phoneNumber', models.CharField(max_length=15)),
                ('dateOfBirth', models.DateField()),
                ('profilePicture', models.ImageField(upload_to='static/media/profile-pictures', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
