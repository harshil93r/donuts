# Generated by Django 2.0.5 on 2018-11-17 16:57

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentAt', models.DateTimeField(auto_now=True)),
                ('messageType', models.CharField(max_length=50, null=True)),
                ('messageBody', models.TextField()),
                ('url', models.URLField(null=True)),
                ('attachmentDisplayName', models.CharField(max_length=100, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participants', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=25), size=None)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='message',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='messagerecipient',
            name='message',
        ),
        migrations.RemoveField(
            model_name='messagerecipient',
            name='messageUserGroup',
        ),
        migrations.RemoveField(
            model_name='messagerecipient',
            name='recipient',
        ),
        migrations.AlterUniqueTogether(
            name='messageusergroup',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='messageusergroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='messageusergroup',
            name='user',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='MessageGroup',
        ),
        migrations.DeleteModel(
            name='MessageRecipient',
        ),
        migrations.DeleteModel(
            name='MessageUserGroup',
        ),
        migrations.AddField(
            model_name='messages',
            name='room',
            field=models.ForeignKey(on_delete=None, to='patient.Rooms'),
        ),
    ]
