from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

USER_ROLE = (
    ('admin','Admin'),
    ('teacher','Teacher'),
    ('student','Student'),
)


class User(AbstractUser): 
    role = models.CharField(max_length=50, choices=USER_ROLE)
    mobile_no = models.CharField(max_length=12)

 