from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

from libgravatar import Gravatar

# Using a custom user manager because the default requires the username parameter.
# This custom user manager is almost identical with the exception of the username requirement being removed.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractUser):
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    first_name = models.CharField(
        max_length=50,
        unique=False,
        blank=False
    )

    last_name = models.CharField(
        max_length=50,
        unique=False,
        blank=False
    )

    email = models.EmailField(
        unique=True,
        blank=False
    )

    bio = models.CharField(
        unique=False,
        max_length=260,
        blank=True
    )

    chess_experience_level = models.IntegerField(
        unique=False,
        blank=False,
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    personal_statement = models.CharField(
        unique=False,
        max_length=520,
        blank=True
    )

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to the user's gravatar."""
        return self.gravatar(60)
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Club(models.Model):

    club_name = models.CharField(
        max_length = 50,
        unique = True,
        blank = False
    )

    location = models.CharField(
        max_length = 100,
        unique = False,
        blank = False

    )

    description = models.CharField(
        unique=False,
        max_length=260,
        blank=True
    )


class Members(models.Model):
    class Meta:
        constraints=[models.UniqueConstraint( fields=["club",'user'], name='member of a club only once')]
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Role(models.IntegerChoices):
        OWNER = 1
        OFFICER = 2
        MEMBER = 3
        APPLICANT = 4
    role = models.IntegerField(choices=Role.choices,
                                default=Role.APPLICANT,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(4)
                                 ])
    def acceptApplicant(self):
        self.role=3
        self.save()
    def denyApplicant(self):
        self.delete()
        
    def officer_promote(self):
        self.role=1
        self.save()
    def officer_demote(self):
        self.role=3
        self.save()
    def member_promote(self):
        self.role=2
        self.save()
    def member_kick(self):
        self.delete()
