from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","content","categories","tags"]

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']