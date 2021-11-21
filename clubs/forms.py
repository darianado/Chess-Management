from django import forms
from django.core.validators import RegexValidator

from clubs.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "bio", "personal_statement", "chess_experience_level"]

class changePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Password",
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
        super().clean()
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if new_password == old_password:
            self.add_error("new_password", "New password cannot match old password")
        elif new_password != password_confirmation:
            self.add_error("password_confirmation", "Confirmation does not match password")
