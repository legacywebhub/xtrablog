# Generated by Django 3.2.2 on 2022-01-21 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_auto_20220119_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='new',
            field=models.BooleanField(default=True),
        ),
    ]
