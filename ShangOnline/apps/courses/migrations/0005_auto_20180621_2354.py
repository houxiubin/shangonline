# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-21 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20180621_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinfo',
            name='need_know',
            field=models.CharField(default='学这门课程要努力努力再努力', max_length=100, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='courseinfo',
            name='teacher_say',
            field=models.CharField(default='好好学习，一定能找到好工作', max_length=200, verbose_name='讲师告知'),
        ),
    ]