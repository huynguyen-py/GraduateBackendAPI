# Generated by Django 3.1.7 on 2021-03-14 02:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Article', '0013_auto_20210314_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date_cmt',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 9, 21, 50, 265438)),
        ),
    ]
