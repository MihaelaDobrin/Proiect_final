from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns =[
    path('', views.HomeIndex.as_view(), name="home"),
    path('add_book/', views.CreateBookIndexView.as_view(), name="add"),
    path('edit_book/<int:pk>/', views.UpdateBookView.as_view(), name="change"),
]