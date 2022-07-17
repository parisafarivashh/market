from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AdminManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Username Can't be empty")
        if not password:
            raise ValueError("Admin Most Have a Password")

        admin = self.model(username=username)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, username, password=None):
        admin = self.create_user(
            username,
            password=password,
        )
        admin.super_admin = True
        admin.save(using=self._db)
        return admin


class Admin(AbstractBaseUser):
    def user_directory_path(self, filename):
        return f'u{self.id}/admin/profile/{filename}'

    phone_regex = RegexValidator(regex=r'09(\d{9})$', message="Enter a valid phone_number. This value may contain only numbers.")
    id = models.AutoField(primary_key=True, verbose_name='شناسه')
    username = models.CharField(max_length=63, unique=True, verbose_name='نام کاربری')
    password = models.CharField(max_length=127, verbose_name='رمز ورود')
    avatar = models.ImageField(upload_to=user_directory_path, verbose_name='عکس پروفایل')
    super_admin = models.BooleanField(default=False, verbose_name='ادمین ارشد')
    first_name = models.CharField(max_length=31, blank=True, null=True, verbose_name='نام ادمین')
    last_name = models.CharField(db_column='LastName', max_length=63, blank=True, null=True, verbose_name='نام خانوادگی ادمین')
    phone_number = models.CharField(db_column='PhoneNumber', max_length=15, unique=True, blank=True, null=True, validators=[phone_regex], verbose_name='شماره تلفن')
    email = models.EmailField(db_column='Email', blank=True, null=True, verbose_name='ایمیل')

    objects = AdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        """ Is the User a member of staff? """
        return self.super_admin

    class Meta:
        verbose_name_plural = 'admin'


@receiver(post_save, sender=Admin)
def create_permissions(sender, instance=None, created=False, **kwargs):
    if created:
        AdminPermissions.objects.create(admin_id=instance)


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
    admin_id = models.OneToOneField(Admin, on_delete=models.CASCADE, verbose_name='admin id ')

    class Meta:
        verbose_name_plural = 'دسترسی های ادمین'
        db_table = 'AdminPermissions'

