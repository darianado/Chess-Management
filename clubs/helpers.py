from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class Role(models.IntegerChoices):
        OWNER = 1
        OFFICER = 2
        MEMBER = 3
        APPLICANT = 4

class Status(models.IntegerChoices):
        NOT_PLAYED = 1, _("Match hasn't been played yet")
        DRAWN = 2, _("Match was drawn")
        WON_A = 3, _("Player A won")
        WON_B = 4, _("Player B won")


