# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 12:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0006_auto_20160606_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='avatar_url',
            new_name='avatar',
        ),
    ]
