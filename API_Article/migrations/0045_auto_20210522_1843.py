# Generated by Django 3.1.7 on 2021-05-22 11:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Article', '0044_auto_20210522_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date_cmt',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 22, 18, 43, 7, 2768)),
        ),
    ]
