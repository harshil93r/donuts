# Generated by Django 2.0.5 on 2018-11-18 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0016_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='formId',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
