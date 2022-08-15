from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AdminManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username:
            raise ValueError("username Can't be empty")
        if not password:
            raise ValueError("Admin Most Have a Password")

        admin = self.model(username=username, phone_number=phone_number)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, username, phone_number, password=None):
        admin = self.create_user(
            username,
            phone_number,
            password=password,
        )
        admin.super_admin = True
        admin.save(using=self._db)
        return admin


class Admin(AbstractBaseUser):
    def user_directory_path(self, filename):
        return f'u{self.id}/admin/profile/{filename}'

    phone_regex = RegexValidator(regex=r'09(\d{9})$', message="Enter a valid phone_number. This value may contain only numbers.")
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=63, unique=True)
    password = models.CharField(max_length=127)
    avatar = models.ImageField(upload_to=user_directory_path)
    super_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=31, blank=True, null=True)
    last_name = models.CharField(db_column='LastName', max_length=63, blank=True, null=True)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=15,
                                    unique=True, blank=False, null=False, validators=[phone_regex])
    email = models.EmailField(db_column='Email', blank=True, null=True)

    objects = AdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    @property
    def is_staff(self):
        """ Is the User a member of staff? """
        return self.super_admin

    def has_perm(self, perm, obj=None):
       return True

    def has_module_perms(self, app_label):
       return True

    class Meta:
        db_table = 'Admin'
        verbose_name_plural = 'admin'
        ordering = ['username']


@receiver(post_save, sender=Admin)
def create_permissions(sender, instance=None, created=False, **kwargs):
    if created:
        AdminPermissions.objects.create(admin_id=instance)


@receiver(post_save, sender=Admin)
def create_user(sender, instance=None, created=False, **kwargs):
    from user.models import User
    if created:
        User.objects.create(phone_number=instance.phone_number)


class AdminPermissions(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    manage_admins = models.BooleanField(default=False, verbose_name='manage other admin')
    wallet = models.BooleanField(default=False, verbose_name='manage wallet ')
    authentication = models.BooleanField(default=False, verbose_name='authentication ')
    top10 = models.BooleanField(default=False, verbose_name='the best')
    reports = models.BooleanField(default=False, verbose_name='reports')
    application_settings = models.BooleanField(default=False, verbose_name='application settings')
    send_message = models.BooleanField(default=False, verbose_name='send message')
    supporter = models.BooleanField(default=False, verbose_name='supporter')
    admin_id = models.OneToOneField(Admin, on_delete=models.CASCADE, verbose_name='admin id')

    class Meta:
        db_table = 'AdminPermissions'
        ordering = ['admin_id']

