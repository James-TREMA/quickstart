from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birthdate']
        widgets = {
            'name': forms.TextInput(attrs={"type": "text", "class": "form-input"}),
            'birthdate': forms.DateInput(attrs={"type": "date", "class": "form-input"}),
        }
        labels = {
            'name': 'Nom',
            'birthdate': 'Date de naissance'
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'published', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'type': 'text'}),
            'published': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Titre',
            'published': 'Date de parution',
            'author': 'Auteur'
        }