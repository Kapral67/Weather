# Generated by Django 3.2.7 on 2021-12-03 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wBE_app', '0002_auto_20211202_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='defaultPage',
            field=models.CharField(blank=True, choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Account', 'Account'), ('Default', 'Default')], max_length=16),
        ),
        migrations.AlterField(
            model_name='account',
            name='measurement',
            field=models.CharField(blank=True, choices=[('SI', 'SI'), ('US', 'US'), ('Default', 'Default')], max_length=16),
        ),
    ]
