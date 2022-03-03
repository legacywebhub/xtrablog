# Generated by Django 3.2.2 on 2022-02-26 16:46

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0005_auto_20220121_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='slug',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='post',
            name='new',
        ),
        migrations.RemoveField(
            model_name='post',
            name='paragraph1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='paragraph2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='paragraph3',
        ),
        migrations.RemoveField(
            model_name='post',
            name='paragraph4',
        ),
        migrations.RemoveField(
            model_name='post',
            name='paragraph5',
        ),
        migrations.AddField(
            model_name='post',
            name='content_body',
            field=ckeditor.fields.RichTextField(default=2, max_length=6000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='content_conclusion',
            field=ckeditor.fields.RichTextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='content_introduction',
            field=ckeditor.fields.RichTextField(default=2, max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='number',
            field=models.PositiveIntegerField(default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image1_url',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image2_url',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image3_url',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='video_url',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='youtube',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='category_name',
            field=models.CharField(choices=[('business', 'Business'), ('technology', 'Technology'), ('internet', 'Internet'), ('tutorials', 'Tutorials'), ('finance', 'Finance'), ('monetary', 'Monetary'), ('online-business', 'Online Business'), ('lifestyle', 'Lifestyle'), ('sports', 'Sports'), ('politics', 'Politics'), ('health', 'Health'), ('science', 'Science'), ('entertainment', 'Entertainment')], max_length=50, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1, editable=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
