from django import forms
from django.contrib.auth import get_user_model
from books.models import *
User = get_user_model()


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('score', 'review')