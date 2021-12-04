from django.shortcuts import render, redirect
from clubs.forms import LogInForm, SignUpForm, EditProfileForm, changePasswordForm, CreateClubForm
from django.contrib.auth import authenticate, login, logout
from clubs.models import Club, User, Members, Events
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
#  from .filters import OrderFilter

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def dashboard(request):
    return render(request, 'partials/dashboard.html')   

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def club_list(request):
    clubs = Club.objects.all()
    return render(request,'club_list.html', {'clubs': clubs})

def show_club(request, club_id):
    try: 
        club = Club.objects.get(id=club_id)
        user = request.user
        member_in_club = Members.get_member_role(user,club)
    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        nr_member = Members.objects.filter(club=club).exclude(role=4).count()
        return render(request,'show_club.html', 
                {'club': club, 'member_in_club': member_in_club, 'number_of_members':nr_member})

def show_applicants(request, club_id):
    try: 
        thisClub = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        applicants = Members.objects.filter(club=thisClub, role=4)
        return render(request,"partials/applicants_as_table.html", 
                 {'club': thisClub, 'applicants':applicants})

def show_roles(request,club_id):
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        users = Members.objects.all().filter(club=club)
        members = users.filter(role = 3)
        officers = users.filter(role = 2)
        return render(request, "partials/roles_list_table.html", {"members": members,"officers": officers})

def members(request, club_id):
    try: 
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        members = [member.user for member in Members.objects.filter(club=club)]
        return render(request, "partials/members_list_table.html", {"members": members})      
      
#@login_required
def show_user(request, user_id=None):
    if user_id is None:
        user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect()
    else:
        show_personal_information = False
        if request.user == user:
            show_personal_information = True
            own_profile = True
        else:
            own_profile = False
            # Get the clubs of the logged in user where they are an officer or owner
            logged_in_user_clubs = [member.club for member in Members.objects.filter(Q(user=request.user) & (Q(role=2) | Q(role=1)))]

            # Check if the user who's profile is being viewed has any clubs in common with the logged in user
            # where the logged in user is an officer or owner
            if Members.objects.filter(user=user, club__in=logged_in_user_clubs).exists():
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

#@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect("show_user", user.id)
    else:
        form = EditProfileForm(instance=user)
    return render(request, "profile.html", {"form": form})

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
                messages.add_message(request, messages.SUCCESS, "Password updated!")
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
                member = Members.objects.create(club=club, user=current_user, role=1)
                return redirect('club_list')
            else:
                return render(request, 'create_club.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()
      
def officer_promote(request,member_id):
    member = Members.objects.get(id=member_id)
    c_id = member.club.id

    member.officer_promote()

    action = Events.objects.create(club=member.club, user=member.user, action = 4)
    return redirect('show_club', club_id = c_id)

def officer_demote(request,member_id):
    member = Members.objects.get(id=member_id)
    c_id = member.club.id

    member.officer_demote()

    action = Events.objects.create(club=member.club, user=member.user, action = 5)
    return redirect('show_club', club_id = c_id)

def member_promote(request,member_id):
    member = Members.objects.get(id=member_id)
    c_id = member.club.id

    member.member_promote()

    action = Events.objects.create(club=member.club, user=member.user, action = 4)
    return redirect('show_club', club_id = c_id)

def member_kick(request,member_id):
    member = Members.objects.get(id=member_id)
    c_id = member.club.id
    club = member.club
    user = member.user

    member.member_kick()

    action = Events.objects.create(club=club, user=user, action = 6)
    return redirect('show_club', club_id = c_id)

def deny_applicant(request, membership_id):
    member = Members.objects.get(id=membership_id)
    c_id = member.club.id
    club = member.club
    user = member.user

    member.denyApplicant()

    action = Events.objects.create(club=club, user=user, action = 3)
    return redirect('show_club', club_id = c_id)

def accept_applicant(request, membership_id):
    member = Members.objects.get(id=membership_id)
    c_id = member.club.id

    member.acceptApplicant()

    action = Events.objects.create(club=member.club, user=member.user, action = 1)
    return redirect('show_club', club_id= c_id)

def events_list(request):
    if request.user.is_authenticated:
        current_user = request.user
        try:
            events = Events.objects.get(user=current_user)
        except ObjectDoesNotExist:
            return redirect('dashboard')
        else:
            return render(request, 'events_list.html', {'events': events})
    else:
        return redirect('log_in')
      
def apply_to_club(request, club_id ):
    club = Club.objects.get(id=club_id)
    user = request.user
    member_in_club = Members.get_member_role(user,club)
    if request.method == 'GET':
        print(" baby one more time")
        Members.objects.create(
                user = user,
                club = club,
                role = 4,
        )

    return redirect('show_club', club.id)

def resend_application(request, club_id):
    club = Club.objects.get(id=club_id)
    user = request.user
    member_in_club = Members.get_member_role(user,club)
    if request.method == 'GET':
        return render(request, 'resend_application.html', 
                {'club': club, 'user':user})
    return redirect('show_club', club.id)

#should be tested after them being a member
def leave_a_club(request, club_id ):
    club = Club.objects.get(id=club_id)
    user = request.user
    member_in_club = Members.get_member_role(user,club)
    if request.method == 'GET':
        print(" baby one more time and i am out of here")
        Members.objects.filter(club_id=club_id).get(user_id=user.id).delete()

    return redirect('show_club', club.id)




def table(request):
    user = request.user
    user_id = user.id 
    #  myFilter = OrderFilter()
    filtered_clubs = []
    filtered_clubs = [member.club for member in Members.objects.filter(Q(user=request.user) )]
    list_data = []
    for club in filtered_clubs:
        
        data_row = (club.club_name, Members.objects.filter(club=club).exclude(role=4).count(), Members.get_member_role_name(Members.get_member_role(user, club)), club.id)
        list_data.append(data_row)
    return render(
            request,
            "table.html",
            {
                "list_data": list_data, 
                #  "myFilter" : myFilter,
            }
        )


