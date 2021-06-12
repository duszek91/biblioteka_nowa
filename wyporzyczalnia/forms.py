from django.forms import ModelForm
from .models import Book
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year', 'release', 'image', 'rate']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
