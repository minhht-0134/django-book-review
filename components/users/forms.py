import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import (
    User,
    Request
)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email đã tồn tại!')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Mật khẩu và xác nhận mật khẩu không khớp nhau")

        return password2

    def save(self, commit=True):
        data = self.cleaned_data

        if User.objects.exists():
            role = 2
        else:
            role = 1

        user = User.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            role=role
        )
        user.set_password(data.get('password1'))
        user.last_login = datetime.datetime.now()
        user.save()

        return user


class LoginForm(forms.Form):
    email = forms.CharField(min_length=1)
    password = forms.CharField(min_length=1)

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(username=cleaned_data.get('email'), password=cleaned_data.get('password'))
        if not user:
            raise ValidationError('Email hoặc mật khẩu không đúng. Vui lòng kiểm tra lại')


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(min_length=1)
    new_password1 = forms.CharField(min_length=1)
    new_password2 = forms.CharField(min_length=1)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Mật khẩu hiện tại không chính xác')

        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Mật khẩu và mật khẩu mới không khớp nhau")

        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)

        if commit:
            self.user.save()

        return self.user


class RequestCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['content']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RequestCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        request_object = super(RequestCreateForm, self).save(commit)

        return request_object


class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['content']
