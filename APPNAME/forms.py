from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","content","categories","post_images","tags"]
        widgets = {
            'post_images': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']