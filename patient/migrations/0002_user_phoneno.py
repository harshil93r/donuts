# Generated by Django 2.0.5 on 2018-11-17 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phoneNo',
            field=models.CharField(default=999999999, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
