# Generated by Django 2.0.5 on 2018-11-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_doctor_insuaranceno'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='license',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
