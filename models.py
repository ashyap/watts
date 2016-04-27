from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100);

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=30);
    lastName = models.CharField(max_length=30);
    birthday = models.DateField();
    shift = models.IntegerField();
    companyId = models.ForeignKey(Company, on_delete=models.CASCADE);
    userType = models.CharField(max_length=30);

class EmployeeLog(models.Model):
    timeIn = models.TimeField(null=True, blank=True);
    timeOut = models.TimeField(null=True, blank=True);
    date = models.DateField(default=timezone.now);
    employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE);
