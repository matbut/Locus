# Generated by Django 2.2.7 on 2019-11-30 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20191124_2037'),
        ('tweetCrawler', '0002_auto_20191126_1854'),
        ('googleCrawlerOfficial', '0002_auto_20191126_2050'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GoogleResultOfficial',
            new_name='InternetResult',
        ),
    ]