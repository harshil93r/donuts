# Generated by Django 2.0.5 on 2018-11-17 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20181117_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
