from django.shortcuts import render, redirect
from .forms import LogInForm, SignUpForm, CreateClubForm
from django.contrib.auth import authenticate, login, logout
from .models import Club, Members
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

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
                return redirect('home')
            else:
                return render(request, 'create_club.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()
