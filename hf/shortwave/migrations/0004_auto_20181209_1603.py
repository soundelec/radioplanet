# Generated by Django 2.1.3 on 2018-12-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortwave', '0003_solardata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solardata',
            name='aindex',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='solardata',
            name='kindex',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='solardata',
            name='solarflux',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='solardata',
            name='sunspots',
            field=models.IntegerField(),
        ),
    ]