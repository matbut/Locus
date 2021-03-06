# Generated by Django 2.2.7 on 2019-12-16 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('search', '0001_initial'),
        ('searchEngine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('link', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=60)),
                ('link', models.URLField()),
                ('avatar', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('username', models.CharField(max_length=60)),
                ('userlink', models.URLField()),
                ('link', models.URLField()),
                ('likes', models.IntegerField()),
                ('replies', models.IntegerField()),
                ('retweets', models.IntegerField()),
                ('hashtags', models.ManyToManyField(to='twitter.Hashtag')),
                ('internet_articles', models.ManyToManyField(related_name='tweets', to='searchEngine.InternetResult')),
                ('searches', models.ManyToManyField(related_name='tweets', to='search.SearchParameters')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='twitter.TwitterUser')),
            ],
        ),
    ]
