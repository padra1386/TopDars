from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput
from django import forms


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        help_text='30 حرف یا کمتر جروف اعداد یا @/./+/-/.',
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'نام کاربری'})
    )

    email = forms.EmailField(
        max_length=254,
        help_text='',
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'ایمیل'})
    )

    password1 = forms.CharField(
        help_text='',
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-user', 'type': 'password', 'placeholder': 'رمز عبور'})
    )

    password2 = forms.CharField(
        help_text='',
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-user', 'type': 'password', 'placeholder': 'تکرار رمز عبور'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-user'}),
            'first_name': TextInput(attrs={'class': 'form-control form-control-user'}),
            'last_name': TextInput(attrs={'class': 'form-control form-control-user'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-user'}),
        }
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
        }
        help_texts = {
            'username': '',
        }
