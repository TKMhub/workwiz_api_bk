from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, userID, email, password=None, **extra_fields):
        if not userID:
            raise ValueError('The User ID field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(userID=userID, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userID, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(userID, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    userID = models.CharField(max_length=50, unique=True, default='default_user')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    addDt = models.DateTimeField(default=timezone.now)
    upDt = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.userID
