
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    ]

    full_name = models.CharField(max_length=100, null=True)
    user_types = models.CharField(choices=USER_TYPES, max_length=100, null=True)

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    Doctor_Types = [
        ('Dentist', 'Dentist'),
        ('Dermatologist', 'Dermatologist'),
    ]
    
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    specialization = models.CharField(choices=Doctor_Types, max_length=100, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"{self.name}-{self.department.name}"


class Patient(models.Model):
    GENDER_TYPES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others', 'Others'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null= True)
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER_TYPES, max_length=100, null=True)
    phone = models.IntegerField(null=True)
    address = models.TextField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}-{self.doctor.name}" 


class Appointment(models.Model):
    Status = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment_date = models.DateTimeField(null=True)
    status = models.CharField(choices=Status, max_length=100, null=True)

    def __str__(self):
        return f"{self.patient} - {self.status}"


    
    
    






  

