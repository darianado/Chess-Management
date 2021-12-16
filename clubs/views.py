from django.shortcuts import render, redirect
from clubs.forms import LogInForm, SignUpForm, EditProfileForm, changePasswordForm, CreateClubForm, CreateTournamentForm, SetMatchResultForm
from django.contrib.auth import authenticate, login, logout
from clubs.models import Club, User, Membership, Events, Tournament, Match, Participant
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from clubs.helpers import Role, Status
from clubs.decorators import login_prohibited, minimum_role_required
from datetime import datetime
from django.utils import timezone


@login_prohibited(redirect_location="dashboard")
def welcome(request):
    '''The welcome page of the chess management system.'''
    user = request.user
    return render(request, 'welcome.html',{'user': user})

def log_out(request):
    '''Function for the user to log out.'''
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('welcome')

@login_prohibited(redirect_location="dashboard")
def log_in(request):
    '''Function for the user to log in.'''
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = next or "dashboard"
                messages.success(request, 'You have logged in.')
                return redirect(redirect_url)
        messages.error(request, 'The credentials provided were invalid!')
    else:
        next = request.GET.get("next") or ""

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'next': next})


@login_required
def dashboard(request):
    user = request.user
    return render(request, 'partials/dashboard.html', {'user': user})

@login_prohibited(redirect_location="dashboard")
def sign_up(request):
    '''Function for the user to sign up.'''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have signed up.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required(redirect_field_name="")
def club_list(request):
    clubs = Club.objects.all()
    return render(request,'club_list.html', {'clubs': clubs})

@login_required(redirect_field_name="")
def show_club(request, club_id):
    '''Function to show details of the club.'''
    try:
        club = Club.objects.get(id=club_id)
        user = request.user
        member_in_club = Membership.get_member_role(user,club)
        owner_club = Membership.objects.get(club=club, role=1)
        nr_member = Membership.objects.filter(club=club).exclude(role=4).count()
        show_role = member_in_club == 1
        show_applicants = member_in_club in [1, 2]
        show_member = member_in_club in [1, 2, 3]

    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        return render(request,'show_club.html',
        {
                'club': club,
                'member_in_club': member_in_club,
                'show_role':show_role,
                'show_member':show_member,
                'show_applicants':show_applicants,
                'number_of_members':nr_member,
                'owner_club' : owner_club,
            }
        )

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location='club_list')
def show_applicants(request, club_id):
    '''Function to show details of applicants.'''
    thisClub = Club.objects.get(id=club_id)
    applicants = Membership.objects.filter(club=thisClub, role=4)
    return render(request,"partials/applicants_as_table.html",
                {'club': thisClub, 'applicants':applicants})

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location='club_list')
def show_roles(request,club_id):
    '''Function to show all officers and members.'''
    club = Club.objects.get(id=club_id)
    users = Membership.objects.all().filter(club=club)
    members = users.filter(role = 3)
    officers = users.filter(role = 2)
    return render(request, "partials/roles_list_table.html", {"members": members,"officers": officers})

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.MEMBER, redirect_location="dashboard")
def members(request, club_id):
    '''Function to show all members.'''
    user = request.user
    club = Club.objects.get(id=club_id)
    is_officer=False
    current_role = Membership.objects.get(user=user,club=club).role
    if current_role==2 or current_role==1:
        is_officer=True
    members = [member.user for member in Membership.objects.filter(club=club, role__lte=Role.MEMBER)]
    return render(request, "partials/members_list_table.html", {"members": members, "is_officer": is_officer})

@login_required
def show_user(request, user_id=None):
    '''Function to show details of users.'''
    if user_id is None:
        user_id = request.user.id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("dashboard")
    else:
        show_personal_information = False
        if request.user == user:
            show_personal_information = True
            own_profile = True
        else:
            own_profile = False
            # Get the clubs of the logged in user where they are an officer or owner
            logged_in_user_clubs = [member.club for member in Membership.objects.filter(Q(user=request.user) & (Q(role=2) | Q(role=1)))]

            # Check if the user who's profile is being viewed has any clubs in common with the logged in user
            # where the logged in user is an officer or owner
            if Membership.objects.filter(user=user, club__in=logged_in_user_clubs).exists():
                show_personal_information = True


        return render(
            request,
            "show_user.html",
            {
                "show_personal_info": show_personal_information,
                "own_profile": own_profile,
                "user_profile": user
            }
        )

@login_required
def profile(request):
    '''Function to change the profile for the user.'''
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            messages.success(request, "Profile updated!")
            form.save()
            return redirect("show_user", user.id)
    else:
        form = EditProfileForm(instance=user)
    return render(request, "profile.html", {"form": form})

@login_required
def password(request):
    '''Function to change password for the user.'''
    current_user = request.user
    if request.method == 'POST':
        form = changePasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('old_password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.success(request, "Password updated!")
                return redirect("show_user", current_user.id)
    else:
        form = changePasswordForm()
    return render(request, 'password.html', {'form': form})

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location="dashboard")
def create_tournament(request, club_id):
    '''Function for the officer and owner to create tournaments.'''
    current_user = request.user
    club = Club.objects.get(id=club_id)
    possible_coorganisers = Membership.objects.filter(Q(club=club) & (Q(role=2) | Q(role=1) )).exclude(user=current_user)

    if request.method == 'GET':
        form = CreateTournamentForm(initial={"coorganisers": possible_coorganisers})
        return render(request, 'create_tournament.html', {'form': form, "club_id": club.id})

    else:
        form = CreateTournamentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            deadline = form.cleaned_data.get('deadline')
            coorganisers = form.cleaned_data.get('coorganisers')

            logged_in_users_membership = Membership.objects.get(club=club, user=current_user)
            coorganisers = form.cleaned_data.get('coorganisers')
            tournament = Tournament.objects.create(name=name, description=description, deadline=deadline, organiser=logged_in_users_membership, club=club)
            tournament.coorganisers.set(coorganisers)
            messages.success(request, "Tournament created successfully!")
            return redirect('dashboard')
        else:
            form = CreateTournamentForm(request.POST, initial={"coorganisers": possible_coorganisers})
            return render(request, 'create_tournament.html', {'form': form, "club_id": club.id })


@login_required(redirect_field_name="")
def create_club(request):
    '''Function for the user to create clubs.'''
    if request.method == 'POST':
        current_user=request.user
        form = CreateClubForm(request.POST)
        if form.is_valid():
            club_name = form.cleaned_data.get('club_name')
            location = form.cleaned_data.get('location')
            description = form.cleaned_data.get('description')
            club = Club.objects.create(club_name=club_name, location=location, description=description)
            member = Membership.objects.create(club=club, user=current_user, role=1)
            messages.success(request, "Club created successfully!")
            return redirect('club_list')
        else:
            return render(request, 'create_club.html', {'form': form})
    else:
        form = CreateClubForm()
        return render(request, 'create_club.html', {'form': form})

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def officer_promote(request,member_id):
    '''Function for the owner to promote an officer.'''
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id
    current_user=request.user
    current_member = Membership.objects.get(user=current_user,club = member.club)

    current_member.demote()
    member.promote()

    Events.objects.create(club=member.club, user=member.user, action = 4)
    messages.success(request, "Officer has been promoted successfully")
    return redirect('show_club', club_id = c_id)

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def officer_demote(request,member_id):
    '''Function for the owner to demote an officer.'''
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id

    member.demote()

    Events.objects.create(club=member.club, user=member.user, action = 5)
    messages.success(request, "Officer has been demoted successfully")
    return redirect('show_club', club_id=c_id)

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def member_promote(request,member_id):
    '''Function for the owner to promote a member.'''
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id

    member.promote()

    Events.objects.create(club=member.club, user=member.user, action = 4)
    messages.success(request, "Member has been promoted successfully")
    return redirect('show_club', club_id = c_id)

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def member_kick(request,member_id):
    '''Function for the owner to kick a member.'''
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id
    club = member.club
    user = member.user

    member.member_kick()

    Events.objects.create(club=club, user=user, action = 6)
    messages.success(request, "Member has been kicked successfully")
    return redirect('show_club', club_id = c_id)

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location="club_list")
def deny_applicant(request, member_id):
    '''Function for the officer to deny an applicants.'''
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id
    club = member.club
    user = member.user

    member.denyApplicant()

    Events.objects.create(club=club, user=user, action = 3)
    messages.success(request, "Applicant has been denied")
    return redirect('show_club', club_id = c_id)

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location="club_list")
def accept_applicant(request,member_id):
    '''Function for the officer to accept an applicants.'''
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id

    member.acceptApplicant()

    Events.objects.create(club=member.club, user=member.user, action = 1)
    messages.success(request, "Applicant has been accepted")
    return redirect('show_club', club_id= c_id)

@login_required(redirect_field_name="")
def events_list(request):
    events = Events.objects.filter(user=request.user)
    return render(request, 'partials/events_list.html', {'events': events})

@login_required(redirect_field_name="")
def apply_to_club(request, club_id ):
    '''Function for an user to apply the club.'''
    club = Club.objects.get(id=club_id)
    user = request.user
    Events.objects.create(club=club, user=request.user, action = 2)
    if request.method == 'GET':
        Membership.objects.create(
                user = user,
                club = club,
                role = 4,
        )
        messages.success(request, 'You have applied the club.')
    return redirect('show_club', club.id)

@login_required(redirect_field_name="")
def leave_a_club(request, club_id ):
    '''Function for an user to leave the club.'''
    club = Club.objects.get(id=club_id)
    user = request.user
    if request.method == 'GET':
        Membership.objects.filter(club_id=club_id).get(user_id=user.id).delete()
        messages.success(request, 'You have left the club.')
    return redirect('show_club', club.id)

@login_required(redirect_field_name="")
def table(request):
    user = request.user
    filtered_clubs = []
    filtered_clubs = [member.club for member in Membership.objects.filter(Q(user=user) )]
    list_data = []
    for club in filtered_clubs:
        data_row = (club.club_name, Membership.objects.filter(club=club).exclude(role=4).count(), Membership.get_member_role_name(Membership.get_member_role(user, club)), club.id)
        list_data.append(data_row)

    return render(request, "table.html", {"list_data": list_data})

@login_required(redirect_field_name="")
def tournament_list(request,club_id):
    user = request.user
    club = Club.objects.get(id=club_id)
    member = Membership.objects.get(user=user,club=club)
    is_officer = False
    if member.role==2 or member.role==1:
        is_officer = True
    tournaments = Tournament.objects.all().filter(club=club)
    return render(request, "partials/tournaments_list_table.html", {"tournaments": tournaments, "is_officer": is_officer, "club": club})

# TODO check if the matches contain the officer -> they do
def matches(request, tournament_id):
    '''Function to match two players.'''
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(tournament=tournament)
    labels = [Status(match.match_status).label for match in matches]

    is_organiser, is_coorganiser = False, False
    if request.user == tournament.organiser.user:
        is_organiser = True
    if request.user in [x.user for x in tournament.coorganisers.all()]:
        is_coorganiser = True
    can_set_match = is_organiser or is_coorganiser

    match_round = tournament.getRoundTournament()
    winner = getWinner(tournament,match_round)
    return render(request, "partials/matches.html", {
        "matches": list(zip(matches, labels)),
        "can_set_match": can_set_match,
        "match_round": match_round,
        "max_rounds" : tournament.getNumberOfRounds(),
        "rounds" : range(1,tournament.getNumberOfRounds()+1),
        "winner" : winner
        }
    )

def updateActiveParticipants(matches):
    '''Function to update active status for playerA and playerB.'''
    for match in matches:
        if match.match_status == 4:
            match.playerA.is_active = False
            match.playerA.save()
        elif match.match_status == 3:
            match.playerB.is_active = False
            match.playerB.save()

def haveDrawn(tournament, match_round):
    '''Function to check if players have a draw in a match.'''
    drawn_round =  Match.objects.filter(tournament=tournament).filter(match_round=match_round).filter(Q(match_status=2))
    return len(drawn_round) > 0

def getWinner(tournament, match_round):
    winner = Participant.objects.filter(tournament=tournament, is_active=True)
    # TODO check the maximum matches possible
    if match_round == tournament.getNumberOfRounds() and len(winner)==1:
        return winner[0]
    return None

def abs(request, tournament, match_round):
    matches = Match.objects.filter(tournament=tournament).filter(match_round=match_round)
    if tournament.isRoundFinished(tournament,match_round):
        updateActiveParticipants(matches)
        tournament.scheduleMatches(match_round+1)
    elif haveDrawn(tournament, match_round):
        messages.error(request, "Set drawn matches again")


@login_required
def set_match_result(request, match_id):
    '''Function to see the match result.'''
    try:
        match = Match.objects.get(id=match_id)
        tournament = match.tournament
        organisers = [coorganiser.user for coorganiser in tournament.coorganisers.all()]
        organisers.append(tournament.organiser.user)
        if request.user not in organisers:
            return redirect("show_tournament", tournament.id)
    except ObjectDoesNotExist:
        return redirect("dashboard")

    players = [
        match.getPlayerA().member.user.get_full_name(),
        match.getPlayerB().member.user.get_full_name()
    ]

    if request.method == 'GET':
        form = SetMatchResultForm(initial={"match_status": match.match_status})
        return render(request, 'set_match_result.html', {'form': form, "match_id" : match_id, "players": players})
    else:
        form = SetMatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            abs(request, match.tournament, match.match_round)
            request.session["on_matches"] = True
            return redirect('show_tournament', tournament.id)
        else:
            return render(request, 'set_match_result.html', {'form': form, "match_id" : match_id, "players": players})

@login_required(redirect_field_name="")
def create_initial_matches(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        organisers = [coorganiser.user for coorganiser in tournament.coorganisers.all()]
        organisers.append(tournament.organiser.user)

        if request.user not in organisers:
            return redirect("show_tournament", tournament.id)
    except ObjectDoesNotExist:
        return redirect("dashboard")

    if tournament.deadline > datetime.now(tz=timezone.utc):
        return redirect("show_tournament", tournament.id)

    if tournament.participants.count() < 2:
        messages.error(request, "Tournament didn't reach at least 2 participants before the deadline so it is now deleted")
        club = tournament.club
        tournament.delete()
        return redirect("show_club", club.id)

    if Match.objects.filter(tournament=tournament).exists():
        return redirect("show_tournament", tournament.id)

    tournament.scheduleMatches(1)
    request.session["on_matches"] = True
    return redirect('show_tournament', tournament.id)

@login_required(redirect_field_name="")
def apply_to_tournament(request, tournament_id ):
    '''Function for the user to apply the tournament.'''
    tournament = Tournament.objects.get(id=tournament_id)
    club = tournament.club
    user = request.user
    member = Membership.objects.get(user=user,club=club)
    member_in_club = Membership.get_member_role(user,club)
    if datetime.now(tz=timezone.utc) < tournament.deadline:
        if tournament.participants.count() < tournament.capacity:
            if request.method == 'GET':
                Participant.objects.create(
                        tournament = tournament,
                        member = member,
                )
            else:
                return redirect('show_tournament', tournament.id)

        else:
            messages.error(request, "Sorry! The capacity for this tournament reached its limit.")
    else:
        messages.error(request, "Sorry! The deadline has passed")

    return redirect('show_tournament', tournament.id)

@login_required(redirect_field_name="")
def leave_tournament(request, tournament_id ):
    '''Function for the user to leave the tournament.'''
    tournament = Tournament.objects.get(id=tournament_id)
    club = tournament.club
    user = request.user
    member = Membership.objects.get(user=user,club=club)
    participant = Participant.objects.get(tournament = tournament, member = member)
    participant.delete()
    return redirect('show_tournament', tournament.id)

@login_required(redirect_field_name="")
def show_tournament(request, tournament_id):
    '''Function to show details of the tournament.'''
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        club = tournament.club
        user = request.user
        organiser = tournament.organiser.user
        participants = tournament.participants.all()
        coorganisers = tournament.coorganisers.all()
        count_participants = tournament.participants.all().count()
        is_organiser = user == organiser
        is_coorganiser = user in [coorganiser.user for coorganiser in coorganisers]
        is_participant = user in [participant.user for participant in participants]
        on_matches = request.session.get("on_matches")
        request.session["on_matches"] = False

        is_before_deadline = datetime.now(tz=timezone.utc) < tournament.deadline
            

    except ObjectDoesNotExist:
            return redirect('club_list')
    return render(request,'show_tournament.html',
        {
            'club': club,
            'is_participant': is_participant,
            'tournament': tournament,
            'organiser': organiser,
            'coorganisers': coorganisers,
            'count_participants': count_participants,
            'is_organiser': is_organiser,
            'is_coorganiser': is_coorganiser,
            'on_matches': on_matches,
            'is_before_deadline': is_before_deadline
        }
    )


@login_required(redirect_field_name="")
def participant_list(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    participants = tournament.participants.all()
    club = tournament.club
    user = request.user
    member = Membership.objects.get(user=user,club=club)
    is_officer = False
    if member.role == 2 or member.role == 1:
        is_officer = True
    return render(request,"partials/participant_list_table.html",
        {
            'is_officer': is_officer,
            'participants': participants,
        }
    )
