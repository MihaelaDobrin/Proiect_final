from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns =[
    path('', views.HomeIndex.as_view(), name="home"),
    path('add_book/', views.CreateBookIndexView.as_view(), name="add"),
    path('edit_book/<int:pk>/', views.UpdateBookView.as_view(), name="change"),
    path('search_book/', views.SearchResultsView.as_view(), name="search"),
    path('', views.ListBookRead.as_view, name='read'),
    path('add_book_read/<int:><int:>', views.CreateBookRead.as_view, name='add_read'),

]