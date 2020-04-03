from django.db import models

# Create your models here.
class Custom_User(models.Model):
    access_code = models.CharField(max_length=25)
    user_type = models.CharField(max_length=5)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    sections = models.CharField(max_length=100)
