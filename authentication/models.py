from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from uuid import uuid4

from .managers import UserManager

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = None
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.TextField(_('First name'))
    last_name = models.TextField(_('Last name'))
    phone_number = models.TextField(_('Phone number'))
    age = models.IntegerField(_('Age'))
    gender = models.TextField(_('Gender'), default='')
    is_employee = models.BooleanField(_('Is user employee?'), default=False)
    is_verified = models.BooleanField(_('Is user verified?'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'gender']

    objects = UserManager()
