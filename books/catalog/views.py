from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from catalog.forms import BooksForm, CommentsForm
from catalog.models import Book, Book_read, Comments
import pandas as pd


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
        kwargs.update({'pk': None})
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

@login_required
def createBookRead(request, pk):
    if Book_read.objects.filter(book_id=pk).exists() is False:
        instance_book = Book_read()
        instance_book.book_id = pk
        instance_book.user_id = request.user.id
        instance_book.save()
        return redirect ('catalog:read')
    return redirect('catalog:home')


class ShowComments(LoginRequiredMixin, ListView):
    model = Comments
    template_name = 'catalog/comments.html'
    context_object_name = 'all_comments'

    def get_context_data(self, **kwargs):
        context = super(ShowComments, self).get_context_data(**kwargs)
        context['all_comments'] = Comments.objects.filter(book_id=self.request.GET.get('id_book'))
        return context


class AddComment(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentsForm
    template_name = 'catalog/comment_form.html'

    def get_form_kwargs(self):
        kwargs = super(AddComment, self).get_form_kwargs()
        kwargs.update({'pk':None})
        kwargs['user'] = self.request.user.id
        kwargs['book'] = self.request.GET.get('id_book')
        return kwargs

    def form_valid(self, form):
        catalog = form.save(commit=False)
        catalog.user_id = self.request.user.id
        catalog.book_id = self.request.GET.get('id_book')
        catalog.save()
        return redirect('catalog:home')











