# Generated by Django 3.0.2 on 2020-01-25 17:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=255, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]