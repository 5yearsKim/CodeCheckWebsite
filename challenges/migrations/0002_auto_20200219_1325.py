# Generated by Django 3.0.2 on 2020-02-19 04:25

import challenges.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(default='a', max_length=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=challenges.models.DescriptionField(),
        ),
    ]
