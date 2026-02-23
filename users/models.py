from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('email is required')
        user = self.model(
            phone=phone,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('terms_agreement', True)
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    full_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=256)
    nationality_code = models.CharField(max_length=10, unique=True)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    terms_agreement = models.BooleanField(null=False, blank=False, default=None)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', ]

    def has_perm(self, app_name):
        return True

    def has_module_perms(self, app_name):
        return True

    @property
    def is_staff(self):
        return self.is_admin