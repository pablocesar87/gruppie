# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-16 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models
import stdimage.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bands', '0007_auto_20170325_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='BandEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name of the event')),
                ('type_event', models.CharField(choices=[('release', 'Release'), ('tour', 'Tour'), ('concert', 'Concert'), ('start_project', 'Start project'), ('merch', 'Merchandising'), ('line_up_change', 'Line up change')], max_length=14, verbose_name='Type of event')),
                ('information', models.TextField(blank=True, verbose_name='Information of the event')),
                ('image', stdimage.models.StdImageField(blank=True, null=True, upload_to=stdimage.utils.UploadToAutoSlugClassNameDir('name'), verbose_name='image')),
                ('date', models.DateTimeField(null=True, verbose_name='Date of the event')),
                ('localization', models.CharField(help_text='Be as accurate as possible if it is a concert.', max_length=256, null=True, verbose_name='Localization of the event')),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='bands.Album', verbose_name='Album')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='bands.Band', verbose_name='Band')),
            ],
            options={
                'verbose_name_plural': 'Band Events',
                'verbose_name': 'Band Event',
            },
        ),
        migrations.CreateModel(
            name='TourDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True, verbose_name='Date of the event')),
                ('localization', models.CharField(help_text='Be as accurate as possible', max_length=256, null=True, verbose_name='Localization of the event')),
                ('extra_info', models.TextField(blank=True, verbose_name='Extra information for this date.')),
            ],
        ),
        migrations.AddField(
            model_name='bandevent',
            name='tour_dates',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bands_events.TourDates'),
        ),
    ]
