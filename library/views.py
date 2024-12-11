from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .forms import AuthorForm, BookForm
from .mixins import PostPermissionMixin

class AuthorList(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AuthorForm()
        return render(
            request,
            'authors.html',
            {'authors': Author.objects.all(), 'form': form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
        messages.error(request, "Erreur dans le formulaire")
        return render(
            request,
            'authors.html',
            {'authors': Author.objects.all(), 'form': form},
        )

class BooksView(PostPermissionMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and '_method' in request.POST:
            pk = request.POST.get('id')
            if pk:
                return self.delete(request, pk, *args, **kwargs)
            else:
                raise Http404("ID is required to delete a book.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = BookForm()
        books_list = Book.objects.all()
        paginator = Paginator(books_list, 10)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)
        return render(
            request,
            'books.html',
            {'form': form, 'books': books},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le livre a été ajouté avec succès.")
            return redirect('books')
        messages.error(request, "Erreur lors de l'ajout du livre.")
        return render(
            request,
            'books.html',
            {'form': form, 'books': Book.objects.all()},
        )

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            messages.success(request, "Le livre a été supprimé avec succès.")
        except Book.DoesNotExist:
            raise Http404("Book does not exist")
        return redirect('books')

@login_required
def author_detail(request: HttpRequest, author_id: int) -> HttpResponse:
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        if 'name' in request.POST:  # Formulaire de modification d'auteur
            author_form = AuthorForm(request.POST, instance=author)
            if author_form.is_valid():
                author_form.save()
                messages.success(request, "Auteur modifié avec succès.")
        elif 'title' in request.POST:  # Formulaire d'ajout de livre
            book_form = BookForm(request.POST)
            if book_form.is_valid():
                book = book_form.save(commit=False)
                book.author = author
                book.save()
                messages.success(request, "Livre ajouté avec succès.")
    else:
        author_form = AuthorForm(instance=author)
        book_form = BookForm()

    return render(
        request,
        'author_detail.html',
        {'author': author, 'author_form': author_form, 'book_form': book_form},
    )

class AuthorDetail(DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = 'author'