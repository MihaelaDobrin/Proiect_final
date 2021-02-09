from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from catalog.forms import BooksForm
from catalog.models import Book


class HomeIndex(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'catalog/catalog_index.html'
    context_object_name = 'all_books'


class CreateBookIndexView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BooksForm
    template_name = 'catalog/catalog_form.html'

    def get_success_url(self):
        return reverse('catalog:home')


class UpdateBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BooksForm
    template_name = 'catalog/catalog_form.html'

    def get_success_url(self):
        return reverse('catalog:change', kwargs={'pk':self.kwargs['pk']})