# Generated by Django 4.1 on 2022-08-18 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("instagram", "0005_bookmark_like_reply"),
    ]

    operations = [
        migrations.RemoveField(model_name="feed", name="like_count",),
    ]
