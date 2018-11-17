from django.db import models

# Create your models here.


class Doctor(models.Model):
    pcpId = models.CharField(max_length=25, null=True)
    rating = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    speciality = models.CharField(max_length=25, null=True)
    license = models.CharField(max_length=20),
    lastseen = models.FloatField()
    insuaranceNo = models.CharField(max_length=20)