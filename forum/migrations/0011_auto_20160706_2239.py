# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_section_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('can_remove_post', 'Can remove a post'),)},
        ),
        migrations.AddField(
            model_name='post',
            name='removed',
            field=models.BooleanField(default=False),
        ),
    ]
