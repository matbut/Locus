# Generated by Django 2.2.2 on 2019-10-14 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleResultOfficial',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('page', models.TextField()),
                ('date', models.DateField()),
                ('link', models.URLField()),
            ],
        ),
    ]