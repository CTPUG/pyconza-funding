# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-02-16 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0002_validators_20191013_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundingapplication',
            name='status',
            field=models.CharField(choices=[('S', 'Submitted'), ('U', 'Under Consideration'), ('F', 'Final Review'), ('G', 'Request Granted'), ('A', 'Offer accepted'), ('R', 'Funding not granted'), ('N', 'Offer not accepted'), ('C', 'Canceled')], default='S', max_length=1),
        ),
    ]
