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

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url
