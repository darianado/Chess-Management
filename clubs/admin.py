from django.contrib import admin
from clubs.models import User, Club, Members, Events

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    list_display = [
        'email', 'first_name', 'last_name', 'is_active', 'bio', 'chess_experience_level', 'personal_statement'
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs"""
    list_display = [
        'club_name', 'location', 'description'
    ]

@admin.register(Members)
class MemberAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for members"""
    list_display = [
        'club', 'user', 'role'
    ]

@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for events"""
    list_display = [
        'club', 'user', 'action'
    ]
