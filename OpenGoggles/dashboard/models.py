from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


PHONE_NUMBER_VALIDATOR = RegexValidator(
    regex = r'^\+?1?\d{9,15}$',
    message = 'Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
)

USERNAME_VALIDATOR = RegexValidator(
    regex = r'^[a-zA-Z0-9_.-]+$',
    message = 'Username must be alphanumeric, with no spaces.'
)


class User(AbstractUser):
    ''' Modified User model from django.contrib.auth.models.User '''

    first_name = models.CharField(
        max_length = 30,
        null = False,
        verbose_name = 'First Name'
    )

    last_name = models.CharField(
        max_length = 30,
        null = False,
        verbose_name = 'Last Name',
    )

    username = models.CharField(
        max_length = 30,
        validators = [USERNAME_VALIDATOR],
        null = False,
        unique = True,
        verbose_name = 'Username'
    )

    email = models.EmailField(
        max_length = 254,
        unique = True,
        verbose_name = 'Email Address'
    )

    phone_number = models.CharField(
        max_length = 12,
        validators = [PHONE_NUMBER_VALIDATOR],
        null = True,
        blank = True,
        verbose_name = 'Phone Number'
    )

    birth_date = models.DateField(
        null = True,
        blank = True,
        verbose_name = 'Birth Date'
    )

    photo_dir = models.CharField(
        max_length = 200,
        null = True,
        blank = True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email