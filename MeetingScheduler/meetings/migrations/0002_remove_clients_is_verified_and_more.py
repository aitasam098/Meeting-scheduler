# Generated by Django 5.1.6 on 2025-06-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='verification_code',
        ),
        migrations.AlterField(
            model_name='clients',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
