# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160530_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='Test'),
            preserve_default=False,
        ),
    ]