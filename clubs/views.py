from django.shortcuts import render

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
def log_in(request):
    return render(request, 'log_in.html')
def sign_up(request):
    return render(request, 'sign_up.html')
