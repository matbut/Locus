# Generated by Django 2.2.7 on 2019-12-12 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('link', models.URLField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='InternetResult',
            fields=[
                ('page', models.TextField()),
                ('date', models.DateField(null=True)),
                ('link', models.URLField(primary_key=True, serialize=False)),
                ('domain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='searchEngine.Domain')),
                ('searches', models.ManyToManyField(related_name='internet_articles', to='search.SearchParameters')),
            ],
        ),
    ]
