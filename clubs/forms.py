from django import forms
from .models import User
from .models import Members
from .models import Club
from django.core.validators import RegexValidator

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'chess_experience_level', 'bio', 'gravatar', 'personal_statement']
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
        self.cleaned_data.get('username'),
        first_name=self.cleaned_data.get('first_name'),
        last_name=self.cleaned_data.get('last_name'),
        email=self.cleaned_data.get('email'),
        bio=self.cleaned_data.get('bio'),
        chess_experience_level=self.cleaned_data.get('chess_experience_level'),
        gravatar=self.cleaned_data.get('gravatar'),
        personal_statement=self.cleaned_data.get('personal_statement'),
        password=self.cleaned_data.get('new_passwords'),
        )
        return user


class LogInForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
