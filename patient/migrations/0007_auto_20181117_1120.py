# Generated by Django 2.0.5 on 2018-11-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_auto_20181117_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='creditcardNo',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='cvv',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='expiryDate',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='insuaranceNo',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pcpId',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='ssn',
            field=models.CharField(max_length=20),
        ),
    ]
