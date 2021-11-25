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
    except ObjectDoesNotExist:
            return redirect('club_list')
    else:
        return render(request,'show_club.html',
                {'club': club })

def role(request,club_id):
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
            return redirect('home')
    else:
        users = Members.objects.all().filter(club=club)
        members = users.filter(role = 3)
        officers = users.filter(role = 2)
        return render(request, "role.html", {"members": members,"officers": officers})
        
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('role')
    else:
        return render(request, 'show_member.html', {'user': user})

def officer_promote(request,member_id):
    c_id=Members.objects.get(id=member_id).club.id
    Members.objects.get(id=member_id).officer_promote()
    return redirect('role', club_id = c_id)

def officer_demote(request,member_id):
    c_id=Members.objects.get(id=member_id).club.id
    Members.objects.get(id=member_id).officer_demote()
    return redirect('role', club_id = c_id)

def member_promote(request,member_id):
    c_id=Members.objects.get(id=member_id).club.id
    Members.objects.get(id=member_id).member_promote()
    return redirect('role', club_id = c_id)

def member_kick(request,member_id):
    c_id=Members.objects.get(id=member_id).club.id
    Members.objects.get(id=member_id).member_kick()
    return redirect('role', club_id = c_id)
