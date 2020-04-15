from django import forms
from .models import Activity

class LoginForm(forms.Form):
  username = forms.CharField(label='User name', max_length=100)
  password = forms.CharField(
    label='Password',
    max_length=100,
    widget=forms.PasswordInput()
  )

class SignupForm(forms.Form):
  username = forms.CharField(label='User name', max_length=100)
  email = forms.EmailField(label='Email', max_length=100)
  password = forms.CharField(
    label='Password',
    max_length=100,
    widget=forms.PasswordInput()
  )

class ActivityAdminForm(forms.ModelForm):
  status = forms.ChoiceField(
    widget=forms.Select(), choices=(Activity.BUY_STATUSES))
