from django.shortcuts import render, redirect
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from .models import Club, Members, User
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
                return redirect('home')
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
    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        return render(request,'show_club.html', 
                 {'club': club})

def show_applicants(request, club_id):
    try: 
        thisClub = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        applicants = Members.objects.filter(club=thisClub, role=4)
        return render(request,'show_club.html', 
                 {'club': thisClub, 'applicants':applicants})

def deny_applicant(request, membership_id):
    Members.objects.get(id=membership_id).denyApplicant()
    return redirect('show_applicants', {'club': membership_id.club})

def accept_applicant(request, membership_id):
    Members.objects.get(id=membership_id).acceptApplicant()
    return redirect('show_applicants', {'club': membership_id.club.id})
