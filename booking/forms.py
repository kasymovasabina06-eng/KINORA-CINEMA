from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignupForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta): model=User; fields=('username','email','password1','password2')
    def clean_email(self):
        value=self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=value).exists(): raise forms.ValidationError('Email уже используется')
        return value
