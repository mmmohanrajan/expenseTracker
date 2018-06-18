from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        # Ensure that an email address is set
        if not email:
            raise ValueError('Users must have a valid e-mail address')

        # Ensure that a username is set
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username')

        account = self.model(
            email=self.normalize_email(email),
            username=kwargs.get('username'),
            mobile=kwargs.get('mobile'),
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password=None, **kwargs):
        if not password:
            raise ValueError('Users must have a valid username')
        account = self.create_user(email, password, kwargs)

        account.is_admin = True
        account.save()

        return account

        
class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile number must be entered in the format: '+919500337503'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']