# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 22:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20160706_2239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('can_remove_post', 'Can remove a post'), ('can_see_poster_ip', 'Can see posters IP address'))},
        ),
    ]
