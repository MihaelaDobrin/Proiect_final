from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns =[
    path('', views.HomeIndex.as_view(), name="home"),
    path('add_book/', views.CreateBookIndexView.as_view(), name="add"),
    path('edit_book/<int:pk>/', views.UpdateBookView.as_view(), name="change"),
    path('search_book/', views.SearchResultsView.as_view(), name="search"),
    path('book_read/', views.ListBookRead.as_view(), name='read'),
    path('add_book_read/<int:pk>', views.createBookRead, name='add_read'),
    path('comments/', views.ShowComments.as_view(), name='list_comments'),
    path('add_new_comment/', views.AddComment.as_view(), name='add_comments'),

]