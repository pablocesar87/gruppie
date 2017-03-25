# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0006_auto_20170325_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='songs',
        ),
        migrations.RemoveField(
            model_name='band',
            name='albums',
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='bands.Band', verbose_name='band'),
        ),
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='bands.Album', verbose_name='album'),
        ),
    ]