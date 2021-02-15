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

    def __init__(self, pk, *args, **kwargs):
        super(BooksForm, self).__init__(*args, **kwargs)
        self.pk = pk

    def clean(self):
        cleaned_data = self.cleaned_data
        title_val= cleaned_data.get('title')
        author_val = cleaned_data.get('author')
        if self.pk:
            if Book.objects.filter(title=title_val, author=author_val).exclude(id=self.pk).exists():
                msg = "Book already exists"
                self.errors['title']=self.error_class([msg])
        else:
            if Book.objects.filter(title=title_val, author=author_val).exists():
                msg = "Book already exists"
                self.errors['title']=self.error_class([msg])

        return cleaned_data








