# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-19 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverifyrecord',
            name='is_expired',
            field=models.BooleanField(default=False, verbose_name='是否过期'),
        ),
    ]