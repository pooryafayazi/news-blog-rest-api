# Generated by Django 4.2.17 on 2025-02-07 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_postcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/%d/'),
        ),
    ]
