from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email.')
        if not fullname:
            raise ValueError('Users must have name.')
        if not phone_number:
            raise ValueError('Users must have phone number.')
        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            fullname=fullname,
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_path(self, filename):
    return f'profile_images/{self.id}/{"profile_image.png"}'


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    username = models.CharField(unique=True, null=True, blank=True, max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fullname = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    phone_number = PhoneNumberField()
    image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
