from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from clubs.models import Club, Members

def login_prohibited(redirect_location):
    def login_prohibited_redirector(view_function):
        def wrapper(request):
            if request.user.is_authenticated:
                return redirect(redirect_location)
            else:
                return view_function(request)
        return wrapper
    return login_prohibited_redirector

def minimum_role_required(role_required, redirect_location):
    def minimum_role_required_redirector(view_function):
        def wrapper(request, club_id):
            try:
                club = Club.objects.get(id=club_id)
                member = Members.objects.get(user=request.user, club=club)

                if member.role <= role_required:
                    return view_function(request, club_id)
                else:
                    return redirect(redirect_location)
            except ObjectDoesNotExist:
                return redirect(redirect_location)

        return wrapper

    return minimum_role_required_redirector