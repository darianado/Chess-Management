from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from math import ceil, log 

from libgravatar import Gravatar
from clubs.helpers import Role, Status

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


class Membership(models.Model):
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=["club", "user"], name="Member of a club only once"),
            models.UniqueConstraint(fields=["club"], condition=Q(role=Role.OWNER), name="Every club has at most 1 owner")
        ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.IntegerField(
        choices=Role.choices,
        default=Role.APPLICANT,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)
        ]
    )

    def acceptApplicant(self):
        self.role=3
        self.save()
    def denyApplicant(self):
        self.delete()

    def promote(self):
        self.role=self.role-1

        self.save()
    def demote(self):
        self.role=self.role+1
        self.save()
    def member_kick(self):
        self.delete()


    def get_member_role(other_user,other_club):
        try:
            member = Membership.objects.filter(club=other_club).get(user=other_user)
        except Membership.DoesNotExist:
            return None
        else:
            return member.role

    def get_member_role_name(role):
        if role == 1:
            return ('Owner')
        elif role == 2:
            return ('Officer')
        elif role == 3:
            return ('Member')
        elif role == 4:
            return ('Applicant')
        elif role == None:
            return ('User')
        return ('')

    def __str__(self):
        return self.user.get_full_name() + " " + self.club.club_name

class Events(models.Model):
    date_created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )
    class Meta:
        ordering = ["-date_created"]
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Action(models.IntegerChoices):
        Accepted = 1
        Applied = 2
        Rejected = 3
        Promoted = 4
        Demoted = 5
        Kicked = 6
        Left = 7
    action = models.IntegerField(choices=Action.choices,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(7)
                                ])
    def getActionString(self):
        if self.action == 1:
            return "Accepted"
        elif self.action == 2:
            return "Applied"
        elif self.action == 3:
            return "Rejected"
        elif self.action == 4:
            return "Promoted"
        elif self.action == 5:
            return "Demoted"
        elif self.action == 6:
            return "Kicked"
        elif self.action == 7:
            return "Left"

    def getActionColour(self):
        if self.action == 1:
            return "green"
        elif self.action == 2:
            return "yellow"
        elif self.action == 3:
            return "red"
        elif self.action == 4:
            return "green"
        elif self.action == 5:
            return "red"
        elif self.action == 6:
            return "red"
        elif self.action == 7:
            return "yellow"

class Tournament(models.Model):

    name = models.CharField(
            max_length = 50,
            unique = True,
            blank = False
    )

    description = models.CharField(
            unique=False,
            max_length=260,
            blank=False
    )

    deadline = models.DateTimeField(
        auto_now=False,
        auto_now_add=False
    )

    organiser = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="organiser")

    coorganisers = models.ManyToManyField(Membership, blank=True)

    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    participants = models.ManyToManyField(Membership, through="Participant", related_name="participants")

    capacity = models.IntegerField(
            unique=False,
            blank=False,
            default=16,
            validators=[
                MinValueValidator(2),
                MaxValueValidator(16)
            ]
        )


    def scheduleMatches(self, match_round):
        all_active_participants = list(Participant.objects.filter(tournament=self, is_active=True))
        all_active_participants.reverse()

        for x in range(0, len(all_active_participants) - 1, 2):
            playerA = all_active_participants[x]
            playerB = all_active_participants[x+1]
            Match.objects.create(
                tournament=self,
                playerA=playerA,
                playerB=playerB,
                match_round=match_round
            )

    def isRoundFinished(self,tournament, match_round):
        matches = Match.objects.filter(match_round=match_round).filter(tournament=tournament)
        for match in matches:
            if match.match_status == 1 or match.match_status==2:
                return False
        return True

    def getNumberOfRounds(self):
        number_participants = Participant.objects.filter(tournament=self).count()
        if number_participants > 0:
            return ceil(log(number_participants,2))
        return 0

    def getRoundTournament(self):
        """Get the current maximum round in the particular tournament """
        matches = Match.objects.filter(tournament=self)
        result_match_round = [match.match_round for match in matches]
        #check if it is 0 when you call it
        return max(result_match_round, default = 0)


class Participant(models.Model):
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=["tournament", "member"], name="Participant of a tournament only once"),
        ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    member = models.ForeignKey(Membership, on_delete=models.CASCADE)

    is_active = models.BooleanField(
        unique=False,
        blank=False,
        default=True
    )

class Match(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(playerA=models.F("playerB")),
                name='players_diff'
            )
        ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    playerA = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="playerA")

    playerB = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="playerB")

    match_status = models.IntegerField(
            choices=Status.choices,
            default=Status.NOT_PLAYED,
            validators=[
                MinValueValidator(1),
                MaxValueValidator(4)
            ]
        )
    match_round = models.IntegerField(
            default=0,
            validators=[
                MinValueValidator(0),
                MaxValueValidator(4)
            ]
        )

    def getPlayerA(self):
        return self.playerA

    def getPlayerB(self):
        return self.playerB
