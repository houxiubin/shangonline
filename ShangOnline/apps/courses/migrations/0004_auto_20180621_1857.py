# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-21 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_courseinfo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinfo',
            name='category',
            field=models.CharField(choices=[('前端', '前端'), ('后端', '后端')], default='前端', max_length=10, verbose_name='课程类别'),
        ),
        migrations.AlterField(
            model_name='courseinfo',
            name='level',
            field=models.CharField(choices=[('初级', '初级'), ('中级', '中级'), ('高级', '高级')], default='初级', max_length=5, verbose_name='课程难度'),
        ),
    ]
