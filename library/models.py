from django.db import models

# Create your models here.
from django import forms


from django.apps import apps

Author = apps.get_model('library', 'Author')
Book = apps.get_model('library', 'Book')

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birthdate']
        widgets = {
            'name': forms.TextInput(attrs={"type": "text", "class": "form-input"}),
            'birthdate': forms.DateInput(
                attrs={"type": "date", "class": "form-input"},
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'name': 'Nom',
            'birthdate': 'Date de naissance',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthdate'].input_formats = ['%Y-%m-%d']


class Book(models.Model):
    title = models.CharField(max_length=200)
    published = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title