from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs_email = User.objects.filter(email__iexact=email)
        if qs_email.exists():
            raise forms.ValidationError("- Cannot use this email. It's already registered")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs_username = User.objects.filter(username__iexact=username)
        if qs_username.exists():
            raise forms.ValidationError("- Cannot use this username. It's already registered")
        return username

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("- Password don't match")
        return password_confirmation

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user