from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(models.Model):
    def user_directory_path(self, filename):
        return f'u{self.id}/profile/{filename}'

    phone_regex = RegexValidator(regex=r'09(\d{9})$', message="Enter a valid phone_number")
    id = models.AutoField(primary_key=True, verbose_name='id')
    username = models.CharField(max_length=255, verbose_name='name', unique=True)
    avatar = models.ImageField(upload_to=user_directory_path, verbose_name='profile picture')
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_regex], verbose_name='phone number')
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    birth_date = models.DateField(blank=True, null=True, verbose_name='birth date')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    last_action = models.DateTimeField(auto_now=True, verbose_name='last action')
    is_authenticated = models.BooleanField(default=False, verbose_name='is authenticated')

    class Meta:
        verbose_name_plural = 'user'
        db_table = 'User'

    @property
    def order(self):
        order = self.orders.filter(paid=False).last()
        return order


class Token(Token):
    user = models.ForeignKey(User, related_name='auth_tokens', on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name_plural = 'token'
        db_table = 'Token'


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Wallet(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    total_amount = models.BigIntegerField(default=0, verbose_name='total amount')
    can_withdraw_amount = models.BigIntegerField(default=0, verbose_name='can withdraw amount  ')
    amount_withdrawn = models.BigIntegerField(default=0, verbose_name='amount withdrawn')
    date = models.DateTimeField(auto_now=True, verbose_name='date')
    user_id = models.OneToOneField(User, models.CASCADE, verbose_name='user id')

    class Meta:
        verbose_name_plural = 'wallet'
        db_table = 'Wallet'


@receiver(post_save, sender=User)
def create_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        Wallet.objects.create(user_id=instance)

