# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-13 10:28
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundingapplication',
            name='accomodation_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total Budget for accomodation while attending PyCon ZA (ZAR)', max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='fundingapplication',
            name='applicant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='funding_application', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fundingapplication',
            name='food_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total Budget for food while attending PyCon ZA (ZAR)', max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='fundingapplication',
            name='local_transport_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total Budget for local transport expenses while attending PyCon ZA (ZAR)', max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='fundingapplication',
            name='other_expenses',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total Budget for other expenses (ZAR). Please explain these expenses in your budget description.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='fundingapplication',
            name='own_contribution',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Amount you can contribute towards attending PyCon ZA (ZAR)', max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='fundingapplication',
            name='travel_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total Budget for travel (ZAR)', max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]