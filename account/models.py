from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    
    class SexChoices(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )

    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    age = models.IntegerField(null=True)
    sex= models.CharField(
        max_length=1,
        choices=SexChoices.choices,
        default=SexChoices.MALE,
        null=True
    )

    def __str__(self):
        return f'{self.username} : {self.user.email}'

"""    def save(self, *args, **kwargs):
        # check a username is provided
        if self.name is None:
            # generate a random username
            self.name = generate_username(1)[0]
        # save the model
        super().save(*args, **kwargs)"""