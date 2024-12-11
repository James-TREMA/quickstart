from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DetailView
from django.shortcuts import render
from django.contrib import messages
from .models import Author, Book
from .forms import AuthorForm, BookForm
from .mixins import PostPermissionMixin

class AuthorList(LoginRequiredMixin, View):
    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == "POST" and not request.user.is_authenticated:
    #         return HttpResponseForbidden("You are not authorized to perform this action.")
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AuthorForm()
        return render(
            request,
            'authors.html',
            { 'authors': Author.objects.all(), 'form': form },
        )
    def post(self, request: HttpRequest)->HttpResponse:
        form = AuthorForm(request.POST)
        if form.is_valid(): # Boom on valide les champs
            form.save()     # Boom enregistrer en bdd
            return HttpResponseRedirect('')
        messages.error(request, "Erreur dans le formulaire")
        return render(
            request,
            'authors.html',
            { 'authors': Author.objects.all(), 'form': form },
        )
    
class BooksView(PostPermissionMixin, View):
    def get(self, request: HttpRequest)->HttpResponse:
        form = BookForm()
        return render(
            request,
            'books.html',
            { 'form': form, 'books': Book.objects.all() },
        )
    
    def post(self, request: HttpRequest)->HttpResponse:
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            form = BookForm()
        return render(
            request,
            'books.html',
            { 'form': form, 'books': Book.objects.all() },
        )

# Create your views here as functions.
@login_required # comes from django.contrib.auth.decorators
def author_detail(request: HttpRequest, author_id: int)->HttpResponse:
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
    return render(
        request,
        'author_detail.html',
        { 'author': author },
    )
    
class AuthorDetail(DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = 'author'