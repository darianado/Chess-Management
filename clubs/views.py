from django.shortcuts import render
from .models import Club
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')


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


