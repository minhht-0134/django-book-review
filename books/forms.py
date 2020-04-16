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

class BookListSearchForm(forms.Form):
  user_id = forms.IntegerField(widget=forms.HiddenInput())
  reading = forms.BooleanField(required=False)
  readed = forms.BooleanField(required=False)
  favorite = forms.BooleanField(required=False)
  pending = forms.BooleanField(required=False)
  approve = forms.BooleanField(required=False)
  reject = forms.BooleanField(required=False)

  title__contains = forms.CharField(label='title', required=False)

  pub_date__gt = forms.DateField(
    label='pub_date_start',
    required=False,
    widget=forms.DateTimeInput
  )
  pub_date__lt = forms.DateField(
    label='pub_date_end',
    required=False,
    widget=forms.DateTimeInput
  )

class ActivityAdminForm(forms.ModelForm):
  status = forms.ChoiceField(
    widget=forms.Select(), choices=(Activity.BUY_STATUSES))
