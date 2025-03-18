from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from viewflow.fields import CompositeKey

class Drug(models.Model):
    name = models.TextField(primary_key=True)
    info = models.TextField()
    child = models.TextField()
    adult = models.TextField()
    women = models.TextField()
    banned = models.TextField()
    why = models.TextField()

    class Meta:
        db_table = 'tblDrug'

class Doctor(models.Model):
    id = models.TextField(primary_key=True)
    mobile = models.TextField()
    name = models.TextField()
    qualification = models.TextField()
    gender = models.TextField()
    address = models.TextField()
    email = models.TextField()
    experience = models.TextField()
    agegroup = models.TextField()
    speciality = models.TextField()

    class Meta:
        db_table = 'tblDoctor'

class DrugDoctor(models.Model):
    id = CompositeKey(columns=['drug_id', 'doctor_id'])
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    unique_together = (('drug', 'doctor'),)

    class Meta:
        db_table = 'tblDrugDoctor'

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions')
