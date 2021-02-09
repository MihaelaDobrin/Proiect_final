from django import forms
from django.forms import TextInput, Select

from catalog.models import Book


class BooksForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'publishing_house']

        widgets = {
            'title': TextInput(attrs={'placeholder': 'Numele cartii', 'class':'form-control'}),
            'author': TextInput(attrs={'placeholder': 'Autorul cartii', 'class':'form-control'}),
            'category': Select(attrs={'class':'form-control'}),
            'publishing_house': Select(attrs={'class':'form-control'}),
        }





