# Generated by Django 2.0.5 on 2018-11-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_doctor_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='lastseen',
            field=models.FloatField(null=True),
        ),
    ]
