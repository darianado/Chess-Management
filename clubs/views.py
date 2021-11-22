from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from clubs.models import User

from clubs.forms import EditProfileForm

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')

#@login_required
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect()
    else:
        return render(request, "show_user.html", {"logged_in_user": request.user, "user_profile": user})

#@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("user/" + user.id)
    else:
        form = EditProfileForm(instance=user)
    return render(request, "profile.html", {"form": form})