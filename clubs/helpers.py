from django.db import models
from django.urls import reverse

class Role(models.IntegerChoices):
        OWNER = 1
        OFFICER = 2
        MEMBER = 3
        APPLICANT = 4

class Status(models.IntegerChoices):
        NOT_PLAYED = 1
        DRAWN = 2
        WON_A = 3
        WON_B = 4


