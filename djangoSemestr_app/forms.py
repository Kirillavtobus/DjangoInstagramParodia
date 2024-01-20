from django import forms
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'id': 'username'})}


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['about', 'image']


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'avatar']
