from django import forms
from .models import Post, Profile, Message, Comment
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
        widgets = {'about': forms.TextInput(attrs={'id': 'about'}),
                   'image': forms.FileInput(attrs={'id': 'image'})
                   }


class ProfilForm(forms.Form):
    about = forms.CharField()
    avatar = forms.FileField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {'comment': forms.TextInput(attrs={
                   'class': "form_e",
                   'placeholder': 'Add a comment...',
                   'id': 'comment'})
                   }


class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {'body': forms.TextInput(attrs={'class': "form_msg", 'placeholder': 'Type'})}


__all__ = ['ChatForm']
