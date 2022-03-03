# Generated by Django 3.2.2 on 2022-03-03 17:08

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_auto_20220226_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content_body',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content_conclusion',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content_introduction',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(default=2, max_length=25000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reply',
            name='reply',
            field=models.TextField(max_length=3000, null=True),
        ),
    ]