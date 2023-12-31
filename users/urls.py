from django.urls import path
from .views import home, profile, RegisterView
from .views import author_list, add_author, quote_list, add_quote
from . import views

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('authors/', views.author_list, name='author_list'),
    path('add_author/', views.add_author, name='add_author'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('add_quote/', views.add_quote, name='add_quote'),

]

