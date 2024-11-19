from django import forms
from django.contrib.auth.forms import UserCreationForm

from custom_auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password1', 'password2']
