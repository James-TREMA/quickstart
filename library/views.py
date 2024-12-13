from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Author, Book
from .forms import AuthorForm, BookForm
from .mixins import PostPermissionMixin
from . import views

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
                    return redirect('author_detail', author_id=author_id)
            elif 'title' in request.POST:  # Formulaire d'ajout de livre
                book_form = BookForm(request.POST)
                if book_form.is_valid():
                    book = book_form.save(commit=False)
                    book.author = author  # Associez le livre à l'auteur actuel
                    book.save()
                    messages.success(request, "Livre ajouté avec succès.")
                    return redirect('author_detail', author_id=author_id)
                else:
                    messages.error(request, "Erreur lors de l'ajout du livre.")
        else:
            author_form = AuthorForm(instance=author)
            # Préremplissez le champ `author` dans le formulaire de livre
            book_form = BookForm(initial={'author': author})

        return render(
            request,
            'library/author_detail.html',
            {
                'author': author,
                'author_form': author_form,
                'book_form': book_form,
            },
        )



    def edit_book(request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                messages.success(request, "Le livre a été modifié avec succès.")
                return redirect('books')  # Redirige vers la liste des livres après modification
        else:
            form = BookForm(instance=book)
        return render(request, 'library/editbook.html', {'form': form, 'book': book})

class AuthorDetail(DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_form'] = AuthorForm(instance=self.object)
        context['book_form'] = BookForm(initial={'author': self.object})
        return context


class AddBookView(View):
    def post(self, request, author_id):
        author = get_object_or_404(Author, id=author_id)
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.author = author
            book.save()
            messages.success(request, "Livre ajouté avec succès.")
        else:
            messages.error(request, "Erreur lors de l'ajout du livre.")
        return redirect('author_detail', author_id=author_id)