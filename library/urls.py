from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list),
    path('books/', views.books_list)
]