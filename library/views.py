from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Author, Book

# Create your views here.
def author_list(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'authors.html',
        { 'authors': Author.objects.all() }
    )

def author_detail(request: HttpRequest, author_id: int)->HttpResponse:
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author)
    return render(
        request,
        'author_detail.html',
        { 'author': author, 'books': books },
    )
    
def books_list(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'books.html',
        { 'books': Book.objects.all() }
    )