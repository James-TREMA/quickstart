from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

urlpatterns = [
    path('authors/<int:author_id>/', views.author_detail),
    path('authors/', views.author_list, name='authors_list'),
    path('books/', views.books_list, name='books_list'),

    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]