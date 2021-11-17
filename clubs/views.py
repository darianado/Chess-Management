from django.shortcuts import render
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     login(request, user)
            #     return redirect('welcome')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
