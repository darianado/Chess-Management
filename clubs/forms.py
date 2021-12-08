from django import forms
from clubs.models import Match, User, Club, Membership, Tournament
from clubs.models import Membership
from clubs.models import Club
from django.core.validators import RegexValidator

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "bio", "personal_statement", "chess_experience_level"]

class changePasswordForm(forms.Form):
    """Form enabling users to change their password."""
    old_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message='Password must contain an uppercase character, a lowercase character and a number'
            )
        ]
    )

    new_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message='Password must contain an uppercase character, a lowercase character and a number'
            )
        ]
    )

    password_confirmation = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message='Password must contain an uppercase character, a lowercase character and a number'
            )
        ]
    )

    def clean(self):
        """Clean the data and generate messages for any errors."""
        super().clean()
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        password_confirmation = self.cleaned_data.get("password_confirmation")


        if new_password == old_password:
            self.add_error("new_password", "New password cannot match old password")
        elif new_password != password_confirmation:
            self.add_error("password_confirmation", "Confirmation does not match password")


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'chess_experience_level', 'bio', 'personal_statement']
        widgets = {'bio': forms.Textarea(), 'personal_statement': forms.Textarea()}

    new_passwords = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput(),
        validators = [RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = 'Password must contain an uppercase character, a lowercase character and a number'
            )
            ]
        )
    password_confirmation = forms.CharField(label = "Password_confirmation", widget= forms.PasswordInput())

    def clean(self):
        super().clean()
        new_passwords = self.cleaned_data.get('new_passwords')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_passwords != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
        first_name=self.cleaned_data.get('first_name'),
        last_name=self.cleaned_data.get('last_name'),
        email=self.cleaned_data.get('email'),
        bio=self.cleaned_data.get('bio'),
        chess_experience_level=self.cleaned_data.get('chess_experience_level'),
        personal_statement=self.cleaned_data.get('personal_statement'),
        password=self.cleaned_data.get('new_passwords'),
        )
        return user


class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    
class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['club_name', 'location', 'description']
        widgets = {'description': forms.Textarea()}

class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'deadline', 'coorganisers', 'capacity']
        widgets = {'description': forms.Textarea(), 'coorganisers' : forms.CheckboxSelectMultiple()}

class SetMatchResultForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["match_status"]
