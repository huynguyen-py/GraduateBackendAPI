# Generated by Django 3.1.7 on 2021-04-30 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Article', '0036_auto_20210316_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content_cmt',
            field=models.TextField(blank=True, default='Body_comment', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_date_cmt',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 30, 22, 13, 42, 6285)),
        ),
    ]
