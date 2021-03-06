# Generated by Django 2.1.3 on 2018-12-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortwave', '0002_auto_20181206_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('solarflux', models.IntegerField(max_length=4)),
                ('aindex', models.IntegerField(max_length=4)),
                ('kindex', models.IntegerField(max_length=4)),
                ('sunspots', models.IntegerField(max_length=4)),
                ('geomagfield', models.CharField(max_length=16)),
                ('signalnoise', models.CharField(max_length=16)),
            ],
        ),
    ]
