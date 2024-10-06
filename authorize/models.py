from datetime import datetime, timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class Manager(BaseUserManager):


    def create_user(self, phone_number, country_code, title, password, **kwargs):
        if title is None:
            raise ValidationError(detail={'error': 'title is null'})
        if password is None:
            raise ValidationError(detail={'error': 'password is null'})
        if country_code is None or phone_number is None:
            raise ValidationError(detail={'error': 'phone number is null'})

        user = self.model(title=title, phone_number=phone_number, country_code=country_code)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, country_code, title, password,
                         **kwargs):
        user = self.create_user(
            phone_number=phone_number,
            country_code=country_code,
            title=title,
            password=password,
            **kwargs,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(update_fields=['is_superuser', 'is_staff'])
        return user


class User(AbstractBaseUser, PermissionsMixin):

    phone_regex = RegexValidator(regex=r'9(\d{9})$', message="Enter a valid phone_number")
    phone_number = models.CharField(validators=[phone_regex], blank=False, null=False, max_length=11)
    country_code = models.IntegerField(blank=False, null=False)
    title = models.CharField(unique=True,max_length=100, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_verify = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'title'
    REQUIRED_FIELDS = ['country_code', 'phone_number']


@receiver(signal=post_save, sender=User)
def admin_created(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser is True:
            Token.objects.create(user=instance)

