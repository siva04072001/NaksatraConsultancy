from email.policy import default
from django.conf import settings 
from django.db import models
from django.contrib.auth.models import AbstractUser





# Create your models here.
class User(AbstractUser):
    userId = models.CharField(max_length=300)
    email = models.EmailField(max_length=5000, unique=True)
    mobNo = models.CharField(max_length=13)
    address = models.TextField(max_length=2000)
    designation = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    


    is_superadmin=models.BooleanField('is superadmin', default=False)
    is_admin=models.BooleanField('is admin', default=False)
    is_engineer=models.BooleanField('is engineer', default=False)
    is_employee=models.BooleanField('is employee', default=False)

class Tickets(models.Model):
    Id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100, blank=True, null=True)
    category=models.CharField(max_length=100, blank=True, null=True)
    location=models.CharField(max_length=100, blank=True, null=True) 
    subfactory=models.CharField(max_length=100, blank=True, null=True)
    item=models.CharField(max_length=100, blank=True, null=True)
    queries=models.CharField(max_length=1000, blank=True, null=True)
    Description=models.TextField(max_length=1000, blank=True, null=True)
    mobileNo=models.CharField(max_length=13, blank=True, null=True)
    mail=models.CharField(max_length=1000, blank=True, null=True)
    priority=models.CharField(max_length=50, blank=True, null=True)
    status=models.CharField(max_length=50,blank=True, null=True)
    assigned=models.CharField(max_length=100,blank=True, null=True)
    assigned_date = models.DateField(blank=True, null=True)
    due_date=models.DateField(blank=True, null=True)
    uploadFile=models.FileField(blank=True, null=True)
    admindesc=models.CharField(max_length=10000,blank=True, null=True)
    issueReport=models.CharField(max_length=10000,blank=True, null=True)
    problemDesc=models.CharField(max_length=10000,blank=True, null=True)
    causeProb=models.CharField(max_length=10000,blank=True, null=True)
    solGiven=models.CharField(max_length=10000,blank=True, null=True)
    notes=models.CharField(max_length=10000,blank=True, null=True)
    expired=models.BooleanField(default=False)

    def __str__(self):
        return self.queries