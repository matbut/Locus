# Generated by Django 2.2.7 on 2019-12-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweetCrawler', '0006_auto_20191201_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='avatar',
            field=models.TextField(default=''),
        ),
    ]
