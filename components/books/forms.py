from pprint import pprint

from django import forms
from .models import (
    Category,
    Book
)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CategoryCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('Danh mục đã tồn tại')

        return name

    def save(self, commit=True):
        self.instance.user = self.user
        category = super(CategoryCreateForm, self).save(commit)

        return category


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Danh mục đã tồn tại')

        return name


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'image',
            'description',
            'publish_date',
            'author',
            'number_page',
            'price',
            'category',
        ]

    def __init__(self, user, files, data):
        self.user = user
        super(BookCreateForm, self).__init__(data, files)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Book.objects.filter(name=name).exists():
            raise forms.ValidationError('Tên sách đã tồn tại')

        return name

    def save(self, commit=True):
        self.instance.user = self.user

        book = super(BookCreateForm, self).save(commit)

        return book


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'image',
            'description',
            'publish_date',
            'author',
            'number_page',
            'price',
            'category',
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Book.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Tên sách đã tồn tại')

        return name
