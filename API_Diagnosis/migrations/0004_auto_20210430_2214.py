# Generated by Django 3.1.7 on 2021-04-30 15:14

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API_Diagnosis', '0003_auto_20210314_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosisrecord',
            name='image_record',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
