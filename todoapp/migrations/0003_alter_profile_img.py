# Generated by Django 4.0.1 on 2022-01-11 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_alter_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Img',
            field=models.FileField(default='', null=True, upload_to='media'),
        ),
    ]
