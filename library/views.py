from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Author

# Create your views here.
def author_list(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'authors.html',
        { 'authors': Author.objects.all() }
    )

def books_list(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'books.html',
        { 'books': Author.objects.all() }
    )