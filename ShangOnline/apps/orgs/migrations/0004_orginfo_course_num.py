# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-25 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0003_orginfo_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='orginfo',
            name='course_num',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
    ]
