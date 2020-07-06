from django.db import models


# Create your models here.

class Medicine(models.Model):  # For storing Medicine info
    mno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/medicines/')
    description = models.TextField()
    price = models.IntegerField()

    def __int__(self):
        return self.mno


class UserType(models.Model):
    user_type = models.CharField(max_length=10)
    username = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class StaffUserInfo(models.Model):  # For storing Staff info
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    address = models.TextField()
    verified_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class DoctorUserInfo(models.Model):  # For storing Doctor info
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    address = models.TextField()
    specialization = models.CharField(max_length=30, unique=True)
    total_appointments = models.IntegerField(default=0)
    treated_appointments = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class PatientUserInfo(models.Model):  # For storing Patient info
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    address = models.TextField()
    total_appointments = models.IntegerField(default=0)
    treated_appointments = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class SellerUserInfo(models.Model):  # For storing Seller info
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    address = models.TextField()
    verified_seller = models.BooleanField(default=False)
    total_no_medicines = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Appointments(models.Model):
    apn = models.AutoField(primary_key=True)
    illness = models.CharField(max_length=50)
    doctor = models.CharField(max_length=30)
    patient = models.CharField(max_length=30)
    issue = models.TextField()
    treated = models.BooleanField(default=False)

    def __int__(self):
        return self.apn


class Specialization(models.Model):
    specialization = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.specialization


class News(models.Model):  # For storing News
    nno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.nno
