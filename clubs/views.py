from django.shortcuts import render, redirect
from clubs.forms import LogInForm, SignUpForm, EditProfileForm, changePasswordForm, CreateClubForm
from django.contrib.auth import authenticate, login, logout
from clubs.models import Club, User, Membership, Events
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, request
from django.contrib.auth.decorators import login_required
#  from .filters import OrderFilter
from clubs.helpers import Role
from clubs.decorators import login_prohibited, minimum_role_required

@login_prohibited(redirect_location="dashboard")
def welcome(request):
    user = request.user
    return render(request, 'welcome.html',{'user': user})

def log_out(request):
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('welcome')

@login_prohibited(redirect_location="dashboard")
def log_in(request):
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
    try:
        club = Club.objects.get(id=club_id)
        user = request.user
        member_in_club = Membership.get_member_role(user,club)
        owner_club = Membership.objects.filter(club=club).get(role=1)
        nr_member = Membership.objects.filter(club=club).exclude(role=4).count()
        show_role = False
        show_member = False
        show_applicants = False
        if member_in_club==1 :
            show_role = True
            show_member = True
            show_applicants = True
        elif member_in_club==2 :
            show_member = True
            show_applicants = True
        elif member_in_club==3 :
            show_member = True

    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        return render(request,'show_club.html',
                {'club': club,
                'member_in_club': member_in_club,
                'show_role':show_role,
                'show_member':show_member,
                'show_applicants':show_applicants,
                'number_of_members':nr_member,
                'owner_club' : owner_club})

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location='club_list')
def show_applicants(request, club_id):
    thisClub = Club.objects.get(id=club_id)
    applicants = Membership.objects.filter(club=thisClub, role=4)
    return render(request,"partials/applicants_as_table.html",
                {'club': thisClub, 'applicants':applicants})


@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location='club_list')
def show_roles(request,club_id):
    club = Club.objects.get(id=club_id)
    users = Membership.objects.all().filter(club=club)
    members = users.filter(role = 3)
    officers = users.filter(role = 2)
    return render(request, "partials/roles_list_table.html", {"members": members,"officers": officers})

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.MEMBER, redirect_location="dashboard")
def members(request, club_id):
    user = request.user
    club = Club.objects.get(id=club_id)
    is_officer=False
    current_role = Membership.objects.get(user=user,club=club).role
    if current_role==2 or current_role==1:
        is_officer=True
    members = [member.user for member in Membership.objects.filter(club=club)]
    return render(request, "partials/members_list_table.html", {"members": members, "is_officer": is_officer})

@login_required
def show_user(request, user_id=None):
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

def create_club(request):
    if request.method =='GET':
        form = CreateClubForm()
        return render(request, 'create_club.html', {'form': form})
    elif request.method == 'POST':
        if request.user.is_authenticated:
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
                messages.error(request, "The credentials provided were invalid!")
                return render(request, 'create_club.html', {'form': form})
        else:
            messages.error(request, "You should log in first")
            return redirect('log_in')


@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def officer_promote(request,member_id):
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id
    current_user=request.user
    current_member = Membership.objects.get(user=current_user,club = member.club)

    current_member.demote()
    member.promote()

    action = Events.objects.create(club=member.club, user=member.user, action = 4)
    messages.success(request, "Officer has been promoted successfully")
    return redirect('show_club', club_id = c_id)

@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def officer_demote(request,member_id):
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id

    member.demote()

    action = Events.objects.create(club=member.club, user=member.user, action = 5)
    messages.success(request, "Officer has been demoted successfully")
    return redirect('show_club', club_id=c_id)


@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def member_promote(request,member_id):
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id

    member.promote()

    action = Events.objects.create(club=member.club, user=member.user, action = 4)
    messages.success(request, "Member has been promoted successfully")
    return redirect('show_club', club_id = c_id)


@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OWNER, redirect_location="club_list")
def member_kick(request,member_id):
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id
    club = member.club
    user = member.user

    member.member_kick()

    action = Events.objects.create(club=club, user=user, action = 6)
    messages.success(request, "Member has been kicked successfully")
    return redirect('show_club', club_id = c_id)


@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location="club_list")
def deny_applicant(request, member_id):
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id
    club = member.club
    user = member.user

    member.denyApplicant()

    action = Events.objects.create(club=club, user=user, action = 3)
    messages.success(request, "Applicant has been denied")
    return redirect('show_club', club_id = c_id)


@login_required(redirect_field_name="")
@minimum_role_required(role_required=Role.OFFICER, redirect_location="club_list")
def accept_applicant(request,member_id):
    member = Membership.objects.get(id=member_id)
    c_id = member.club.id

    member.acceptApplicant()

    action = Events.objects.create(club=member.club, user=member.user, action = 1)
    messages.success(request, "Applicant has been accepted")
    return redirect('show_club', club_id= c_id)

@login_required(redirect_field_name="")
def events_list(request):
    events = Events.objects.filter(user=request.user)
    return render(request, 'partials/events_list.html', {'events': events})

@login_required(redirect_field_name="")
def apply_to_club(request, club_id ):
    club = Club.objects.get(id=club_id)
    user = request.user
    member_in_club = Membership.get_member_role(user,club)
    Events.objects.create(club=club, user=request.user, action = 2)
    if request.method == 'GET':
        Membership.objects.create(
                user = user,
                club = club,
                role = 4,
        )
<<<<<<< HEAD
        messages.success(request, 'You have applied the club.')
=======
    messages.success(request, 'You have applied to the club.')
>>>>>>> main
    return redirect('show_club', club.id)


@login_required(redirect_field_name="")
def leave_a_club(request, club_id ):
    club = Club.objects.get(id=club_id)
    user = request.user
    member_in_club = Membership.get_member_role(user,club)
    if request.method == 'GET':
        Membership.objects.filter(club_id=club_id).get(user_id=user.id).delete()
        messages.success(request, 'You have left the club.')
    return redirect('show_club', club.id)

@login_required(redirect_field_name="")
def table(request):
    user = request.user
    user_id = user.id
    #  myFilter = OrderFilter()
    filtered_clubs = []
    filtered_clubs = [member.club for member in Membership.objects.filter(Q(user=user) )]
    list_data = []
    for club in filtered_clubs:

        data_row = (club.club_name, Membership.objects.filter(club=club).exclude(role=4).count(), Membership.get_member_role_name(Membership.get_member_role(user, club)), club.id)
        list_data.append(data_row)

    return render(
            request,
            "table.html",
            {
                "list_data": list_data,
                #  "myFilter" : myFilter,
            }
        )
