# Generated by Django 1.11.4 on 2017-10-17 07:25


import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('app', '0013_auto_20171017_0724')]

    operations = [
        migrations.AlterField(
            model_name='chain',
            name='sid',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='chain_sid',
                to='app.IdNamespace',
            ),
        )
    ]
