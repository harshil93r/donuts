# Generated by Django 2.0.5 on 2018-11-17 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_doctor_lastseen'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='insuaranceNo',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]