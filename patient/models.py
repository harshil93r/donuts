from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Patient(models.Model):
    GENDER_TYPES = [('M', 'Male'), ('F', 'Female'),
                    ('O', 'Other'), ('U', 'Unknown')]
    STATUS_TYPES = [('ACTIVE', 'ACTIVE'), ('DELETED', 'DELETED')]
    patientId = models.CharField(max_length=25, null=False)
    firstName = models.CharField(max_length=100, null=False)
    lastName = models.CharField(max_length=100, null=False)
    gender = models.CharField(
        max_length=50, choices=GENDER_TYPES, default='Unknown', null=False)
    dob = models.DateField(null=False)
    primaryCell = models.CharField(max_length=25, null=False)
    email = models.EmailField(null=True)
    zip5 = models.CharField(max_length=10)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    insuaranceNo = models.CharField(max_length=15)
    creditcardNo = models.CharField(max_length=16)
    expiryDate = models.CharField(max_length=6)
    cvv = models.PositiveIntegerField()
    pcpId = models.CharField(max_length=15)
    ssn = models.TextField()
    appUserId = models.TextField()


class User(AbstractUser):
    """
    Required Fields:
        -   username
        -   empi
        -   date_of_birth
        -   tenant_id
    """

    _type = models.CharField(max_length=1, null=False)
    doctor = models.ForeignKey('doctor.Doctor', on_delete=None)
    patient = models.ForeignKey(Patient, on_delete=None)

    class Meta(object):
        db_table = 'auth_user'
