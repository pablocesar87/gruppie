# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 15:43
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='album_song', to='bands.Song', verbose_name='songs'),
        ),
        migrations.AddField(
            model_name='song',
            name='length_minutes',
            field=models.PositiveIntegerField(null=True, verbose_name='minutes lentgh'),
        ),
        migrations.AddField(
            model_name='song',
            name='length_seconds',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(59)], verbose_name='seconds lentgh'),
        ),
    ]