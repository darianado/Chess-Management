from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from clubs.models import User

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')

#@login_required
def user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect()
    else:
        return render(request, "show_user.html", {"logged_in_user": request.user, "user_profile": user})

#@login_required
def edit_profile(request, user_id):
    return redirect("user_profile", user_id)