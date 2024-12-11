from django.urls import path
from . import views

urlpatterns = [
    # path('authors/<int:author_id>/', views.author_detail),
    path('authors/alone/<int:pk>/', views.AuthorDetail.as_view()),
    path('authors/', views.AuthorList.as_view()),
    path('books/', views.BooksView.as_view(), name="books"),
    path('books/<int:pk>/delete', views.BooksView.as_view(), name="delete_book"),


    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]