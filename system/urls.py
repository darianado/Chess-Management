"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name = 'welcome'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('log_out/', views.log_out, name='log_out'),

    path('home/dashboard', views.dashboard, name = 'dashboard'),
    path('home/clubs', views.club_list, name = 'club_list'),



    # path('clubs/', views.club_list, name = 'club_list'),
    path('club/<int:club_id>', views.show_club, name = 'show_club'),
    path('club/<int:club_id>/members/', views.members, name = 'show_members'),
    path('user/<int:user_id>', views.show_user, name="show_user"),
    path('user/', views.show_user, name="show_user"),
    path('profile/', views.profile, name="profile"),
    path('password/', views.password, name="password"),

    path('create_club/', views.create_club, name = 'create_club'),
    path('create_tournament/<int:club_id>', views.create_tournament, name = 'create_tournament'),
    #  path('create_tournament/<int:club_id>', views.create_tournament, name = 'tournament'),

    path('club/<int:club_id>/roles', views.show_roles, name = 'show_roles'),
    path('officer_promote/<int:member_id>', views.officer_promote, name = 'officer_promote'),
    path('officer_demote/<int:member_id>', views.officer_demote, name = 'officer_demote'),
    path('member_promote/<int:member_id>', views.member_promote, name = 'member_promote'),
    path('member_kick/<int:member_id>', views.member_kick, name = 'member_kick'),

    path('apply/<int:club_id>', views.apply_to_club, name = 'apply_to_club'),
    path('leave_a_club/<int:club_id>', views.leave_a_club, name = 'leave_a_club'),
    path('resend_application/<int:club_id>', views.resend_application, name = 'resend_application'),

    path('deny_applicant/<int:member_id>', views.deny_applicant, name = 'deny_applicant'),
    path('accept_applicant/<int:member_id>', views.accept_applicant,name = 'accept_applicant'),
    path('club/<int:club_id>/applicants', views.show_applicants, name = 'show_applicants'),


    path('table/', views.table, name="table"),
    path('events/', views.events_list, name="events_list"), 
    path('matches/', views.matches, name="matches"),
]
