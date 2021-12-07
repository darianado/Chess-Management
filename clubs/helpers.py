from django.db import models
from django.urls import reverse

class Role(models.IntegerChoices):
        OWNER = 1
        OFFICER = 2
        MEMBER = 3
        APPLICANT = 4
