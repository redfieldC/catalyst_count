from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)

class Company(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # file = models.FileField(upload_to='uploads/')
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250)
    domain = models.CharField(max_length=250)
    year = models.PositiveIntegerField(default=2021)
    industry = models.TextField(default='UNKNOWN')
    size_range = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.CharField(max_length=250, default='Unknown')
    linkedin_url = models.CharField(max_length=250)
    current_employee_estimate = models.IntegerField()
    total_employee_estimate = models.IntegerField()