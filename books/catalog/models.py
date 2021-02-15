from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Book(models.Model):

    category_choices = (('Literatura', 'Literatura'), ('Economie', 'Economie'), ('Dezvoltare personala', 'Dezvoltare personala'))
    publishing_choices = (('Litera', 'Litera'), ('Nemira', 'Nemira'), ('Curtea Veche', 'Curtea veche'))

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=category_choices)
    publishing_house =models.CharField(max_length=100, choices=publishing_choices)
    # rating = models.FloatField(default=None)

    def __str__(self):
        return f'{self.title} de {self.author} '


class Book_read(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book.title}'

class Rating(models.Model):

    rating_book = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.book.title} - {self.rating_book}'


class Comments(models.Model):

    comment_added = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #
    # def __str__(self):
    #     return f'{self.comment_added} by {self.user_id.name} for {self.book_id.name}'