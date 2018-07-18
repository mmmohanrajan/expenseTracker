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
    '''
    '''
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile number must be entered in the format: '+919500337503'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], unique=True, blank=True, null=True, max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Group(models.Model):
    '''
    '''
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='group_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='users_list')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_on',)


class Activity(models.Model):
    '''
    '''
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    description = models.TextField(max_length=150, blank=True)
    amount = models.FloatField(blank=False)
    gid = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='activity_group')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    except_users = models.ManyToManyField(User, related_name='except_users', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_created_by')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_on',)


class Comment(models.Model):
    activity = models.ForeignKey(Activity, blank=True, on_delete=models.CASCADE, related_name='cmt_activity')
    content = models.TextField(max_length=150)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cmt_createdby')
    created_on = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    '''
    '''
    total = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acc_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='acc_group')

    class Meta:
        unique_together = ('user', 'group',)