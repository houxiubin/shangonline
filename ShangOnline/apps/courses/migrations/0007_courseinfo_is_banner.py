# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-25 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20180622_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinfo',
            name='is_banner',
            field=models.BooleanField(default=True, verbose_name='是否轮播'),
        ),
    ]