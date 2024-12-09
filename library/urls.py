from django.urls import path
from . import views

urlpatterns = [
    path('authors/<int:author_id>/', views.author_detail),
    path('authors/', views.author_list),
    path('books/', views.books_list)
]