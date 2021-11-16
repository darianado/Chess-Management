from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ symbol followed by at least 3 alphanumericals'
        )]
    )

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

    gravatar = models.ImageField(
        upload_to="gravatar_uploads/",
        blank=True
    )


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
