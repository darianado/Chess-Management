from django.shortcuts import render, redirect
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from .models import Club, Members
from django.core.exceptions import ObjectDoesNotExist

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
                return redirect('welcome')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def home(request):
    return render(request, 'home.html')   

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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
        return render(request,'show_club.html', 
                {'club': club, 'member_in_club': member_in_club})

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
