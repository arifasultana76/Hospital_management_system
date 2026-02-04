
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractUser

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

    name = models.CharField(max_length=100, null=True)
    specialization = models.CharField(choices=Doctor_Types, max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    GENDER_TYPES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER_TYPES, max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


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







# class CustomUser(AbstractUser):
#     USER_TYPES=[
#         ('Admin','Admin'),
#         ('Doctor','Doctor'),
#         ('Patient','Patient',)
#     ]
    
#     full_name=models.CharField(max_length=100, null=True)
#     user_types=models.CharField(choices=USER_TYPES,max_length=100, null=True)

#     def __str__(self):
#         return self.full_name
    
# class Department(models.Model):
#     name=models.CharField(max_length=100, null=True)
#     location=models.CharField(max_length=100, null=True)

#     def __str__(self):
#         return self.name
    
# class Doctor(models.Model):
#     name=models.CharField(max_length=100, null=True)
#     Doctor_Types=[
#         ('Dentist','Dentist'),
#         ('Dermatologist','Dermatologist'),
#     ]
#     specialization=models.CharField(choices=Doctor_Types,max_length=100, null=True)
#     phone=models.CharField(max_length=100, null=True)
#     email=models.EmailField(null=True)
#     department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)

#     def __str__(self):
#         return self.name
    

# class Patient(models.Model):
#     name=models.CharField(max_length=100, null=True)
#     age=models.IntegerField(null=True)
#     GENDER_TYPES=[
#         ('Female','Female'),
#         ('Male','Male'),
#         ('Others','Others'),
#     ]

#     gender=models.CharField(choices=GENDER_TYPES,max_length=100, null=True)
#     phone=models.CharField(max_length=100, null=True)
#     address=models.TextField(null=True)
#     doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)

#     def __str__(self):
#         return self.name  

# class Appointment(models.Model):
#     patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
#     doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
#     appointment_date=models.DateTimeField(null=True)
#     Status=[
#         ('Pending','Pending'),
#         ('Completed','Completed'),
#         ('Cancelled','Cancelled'),
#     ]
#     status=models.CharField(choices=Status,max_length=100, null=True)

#     def __str__(self):
#         return f'{self.name}-{self.status}' 
    
    
    
    






  

