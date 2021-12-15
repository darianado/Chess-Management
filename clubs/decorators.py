from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from clubs.models import Club, Membership

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
        def wrapper(request, *, club_id=None, member_id=None):
            try:
                if member_id is None:
                    club = Club.objects.get(id=club_id)
                else:
                    club = Membership.objects.get(id=member_id).club

                id = club_id or member_id
                member = Membership.objects.get(user=request.user, club=club)

                if member.role <= role_required:
                    return view_function(request, id)
                else:
                    return redirect(redirect_location)
            except ObjectDoesNotExist:
                return redirect(redirect_location)

        return wrapper

    return minimum_role_required_redirector

def exact_role_required(role_required, redirect_location):
    def exact_role_required_redirector(view_function):
        def wrapper(request, club_id):
            try:
                club = Club.objects.get(id=club_id)
                member = Membership.objects.get(user=request.user, club=club)

                if member.role == role_required:
                    return view_function(request, club_id)
                else:
                    return redirect(redirect_location)
            except ObjectDoesNotExist:
                return redirect(redirect_location)

        return wrapper

    return exact_role_required_redirector
