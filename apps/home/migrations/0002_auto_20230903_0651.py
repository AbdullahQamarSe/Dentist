# Generated by Django 3.2.6 on 2023-09-03 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='additional_image',
            field=models.ImageField(blank=True, null=True, upload_to='additional_images/'),
        ),
        migrations.AlterField(
            model_name='case',
            name='upper_jaw_image',
            field=models.ImageField(blank=True, null=True, upload_to='upper_jaw_images/'),
        ),
    ]
