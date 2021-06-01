from django.contrib import admin
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        if username is None:
            raise TypeError("Users should have an Username")
        if email is None:
            raise TypeError("Users should have an Email")
        user = self.model(username=username, first_name="first_name", last_name="last_name", email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should be not None")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    first_name = models.CharField(max_length=255, blank=False, default="Anonymous")
    last_name = models.CharField(max_length=255, blank=False, default="User")
    phone = models.CharField(max_length=11, default="0348387208")
    address = models.CharField(max_length=500, default="Can Tho")
    avatar = CloudinaryField('avatar')
    Followed = models.ManyToManyField('self', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def total_follow(self):
        return self.Followed.count()

admin.site.register(User)
