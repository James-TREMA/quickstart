from django.urls import path
from . import views

urlpatterns = [
    path('authors/<int:author_id>/', views.author_detail),
    path('authors/alone/<int:pk>/', views.AuthorDetail.as_view()),
    path('authors/', views.AuthorList.as_view()),
    path('books/', views.BooksView.as_view(), name="books"),
    path('books/<int:pk>/delete', views.BooksView.as_view(), name="delete_book"),
]