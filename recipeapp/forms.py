from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].required = False  # Remove password2
        self.fields.pop('password2', None)         # Remove from form
        for field in self.fields.values():
            field.help_text = None  # Remove help texts
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']

class AboutForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about']