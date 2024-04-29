from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        """
        Creates and saves a User with the given email, fullname, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None):
        """
        Creates and saves a superuser with the given email, fullname, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(verbose_name="Full Name", max_length=60)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(verbose_name="Bio", blank=True, null=True)
    mobile = models.CharField(verbose_name="Phone No", max_length=16, blank=True, null=True)
    facebook_id = models.CharField(verbose_name="Facebook ID", max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    account_creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    class Meta:
        ordering = ['-account_creation_date']
        permissions = [
            ("editing_access", "Can edit food items and  orders"),
        ]

    def __str__(self):
        return self.fullname

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class UserAddress(models.Model):
    user = models.ForeignKey(MyUser, related_name="address", on_delete=models.CASCADE)
    country = models.CharField(max_length=255, verbose_name="Country")
    postal_code = models.CharField(max_length=32, verbose_name="Postal Code")
    address = models.TextField(max_length=400, verbose_name="Address")
    is_default = models.BooleanField(verbose_name="Default Address", default=True)
