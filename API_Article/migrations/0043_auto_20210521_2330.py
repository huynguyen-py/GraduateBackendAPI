# Generated by Django 3.1.7 on 2021-05-21 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Article', '0042_auto_20210521_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date_cmt',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 21, 23, 30, 15, 892282)),
        ),
        migrations.AlterField(
            model_name='reportdetail',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 21, 23, 30, 15, 896270)),
        ),
    ]
