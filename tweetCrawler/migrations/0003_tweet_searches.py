# Generated by Django 2.2.2 on 2019-11-13 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
        ('tweetCrawler', '0002_auto_20190513_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='searches',
            field=models.ManyToManyField(to='search.SearchParameters'),
        ),
    ]