# Generated by Django 3.1.7 on 2021-03-14 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Article', '0029_auto_20210314_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date_cmt',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 14, 29, 19, 212101)),
        ),
    ]
