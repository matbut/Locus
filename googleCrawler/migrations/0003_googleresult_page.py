# Generated by Django 2.2.2 on 2019-10-07 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googleCrawler', '0002_auto_20190617_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='googleresult',
            name='page',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]
