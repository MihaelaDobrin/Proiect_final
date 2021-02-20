from django import forms
from django.forms import TextInput, Select

from catalog.models import Book, Comments


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


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['comment_added', 'rating']

        widgets = {
            'comment_added': TextInput(attrs={'placeholder': 'Content of comment', 'class': 'form-control'}),
            'rating': Select(attrs={'placeholder': 'Stars', 'class': 'form-control'}),
        }

    def __init__(self, pk, book, user, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.pk = pk
        self.book = book
        self.user = user

    def clean(self):
        cleaned_data = self.cleaned_data
        comment_val =cleaned_data.get('comment_added')
        rating_val =cleaned_data.get('rating')
        if Comments.objects.filter(user_id=self.user).exists():
            msg = 'Userul a postat deja un comentariu pentru aceasta carte'
            self.errors['comment_added']=self.error_class([msg])
        elif comment_val is None:
            msg = 'Userul nu a completat'
            self.errors['comment_added'] = self.error_class([msg])
        elif rating_val is None:
            msg = 'Userul nu a completat'
            self.errors['rating'] = self.error_class([msg])

        return cleaned_data











