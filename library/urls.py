from django.urls import path
from . import views

urlpatterns = [
    path('authors/alone/<int:pk>/', views.AuthorDetail.as_view(), name="author_alone"),
    path('authors/', views.AuthorList.as_view(), name="author_list"),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author_detail'),

    path('books/', views.BooksView.as_view(), name="books"),
    path('books/<int:book_id>/edit/', views.BooksView.as_view(), name='edit_book'),
    path('books/<int:book_id>/delete/', views.BooksView.as_view(), name='delete_book'),
]