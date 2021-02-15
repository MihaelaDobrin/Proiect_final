from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from catalog.forms import BooksForm
from catalog.models import Book, Book_read


class HomeIndex(ListView):
    model = Book
    template_name = 'catalog/catalog_index.html'
    context_object_name = 'all_books'


class CreateBookIndexView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BooksForm
    template_name = 'catalog/catalog_form.html'

    def get_form_kwargs(self):
        kwargs = super(CreateBookIndexView, self).get_form_kwargs()
        kwargs.update({'pk':None})
        return kwargs

    def get_success_url(self):
        return reverse('catalog:home')


class UpdateBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BooksForm
    template_name = 'catalog/catalog_form.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateBookView, self).get_form_kwargs()
        kwargs.update({'pk':self.kwargs['pk']})
        return kwargs


    def get_success_url(self):
        return reverse('catalog:change', kwargs={'pk':self.kwargs['pk']})


class SearchResultsView(ListView):
    model = Book
    template_name = 'catalog/search_book.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        book_list = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return book_list

class ListBookRead(LoginRequiredMixin, ListView):
    model = Book_read
    template_name = 'catalog/books_read.html'
    context_object_name = 'books_read'


class CreateBookRead(CreateView):
    model = Book_read
    fields = ['book', 'user']







