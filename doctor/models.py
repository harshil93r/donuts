from django.db import models

# Create your models here.
class Doctor(models.Model):
	ssn = models.CharField(max_length=10, null=True)
	pcpId = models.CharField(max_length=10, null=True)
	insuranceNo = models.CharField(max_length=10, null=True)
	credtardNo = models.CharField(max_length=16, null=True)