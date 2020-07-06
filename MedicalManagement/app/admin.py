from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Medicine)

admin.site.register(models.UserType)

admin.site.register(models.StaffUserInfo)

admin.site.register(models.DoctorUserInfo)

admin.site.register(models.PatientUserInfo)

admin.site.register(models.SellerUserInfo)

admin.site.register(models.Appointments)

admin.site.register(models.Specialization)

admin.site.register(models.News)
