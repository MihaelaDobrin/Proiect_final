from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import request, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
import xlwt
import datetime
import json

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

def book_export(request):
    # data_source = {}
    # data_source['title'] = []
    # data_source['author'] = []
    # data_source['category'] = []
    # data_source['publishing_house'] = []
    if request.user.is_superuser == 1:
        data_book = Book.objects.all()
        # list_title = []
        # list_author = []
        # list_category = []
        # list_publishing_house = []
        list_data = []
        for item in data_book:
            list_work = []
            list_work.append(item.title)
            list_work.append(item.author)
            list_work.append(item.category)
            list_work.append(item.publishing_house)
            list_data.append(list_work)
            # list_title.append(item.title)
            # list_author.append(item.author)
            # list_category.append(item.category)
            # list_publishing_house.append(item.publishing_house)
        # data_source['title'] = list_title
        # data_source['author'] = list_author
        # data_source['category'] = list_category
        # data_source['publishing_house'] = list_publishing_house
        response = HttpResponse (content_type = 'application/ms-excel')
        filename = 'List of books_{}.xls'
        content = "attachment; filename =%s" % filename
        response['Content-Disposition'] = content
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('List of books_')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        # columns = [key for key in data_source]
        columns = ['title', 'author', 'category', 'publishing_house']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for row in range (len(list_data)):
            row_num += 1
            for col_num in range(len(columns)):
                ws.write(row_num, col_num,list_data[row][col_num], font_style)
        wb.save(response)
        return response
    else:
        return redirect('catalog:home')














