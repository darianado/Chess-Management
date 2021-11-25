from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clubs.forms import LogInForm, SignUpForm, EditProfileForm, changePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from clubs.models import Members, User
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    return render(request, 'home.html')

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

#@login_required
def show_user(request, user_id):
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
