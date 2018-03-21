# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 01:37


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_mediatype_mediatypeproperty'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesIdToHeadPersistentId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seriesidtoheadpersistentid_pid', to='app.IdNamespace')),
                ('sid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seriesidtoheadpersistentid_sid', to='app.IdNamespace')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesIdToPersistentId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seriesidtopersistentid_pid', to='app.IdNamespace')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seriesidtopersistentid_sid', to='app.IdNamespace')),
            ],
        ),
        migrations.RemoveField(
            model_name='seriesidtoscienceobject',
            name='sciobj',
        ),
        migrations.RemoveField(
            model_name='seriesidtoscienceobject',
            name='sid',
        ),
        migrations.DeleteModel(
            name='SeriesIdToScienceObject',
        ),
    ]
