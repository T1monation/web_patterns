# Generated by Django 3.0.7 on 2020-07-04 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20200704_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='repaid_len',
            field=models.PositiveIntegerField(default=1, verbose_name='длительность ремонта в днях'),
        ),
    ]