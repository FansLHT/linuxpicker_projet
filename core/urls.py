# core/urls.py

from django.urls import path
from .views import (
    index, tutoriels, distribution_detail,
    quiz_recommandation, # Importez la nouvelle vue du quizz
    # Note: 'rechercher_distribution' n'est plus nécessaire si 'index' gère le filtrage/recherche
)
from . import views

urlpatterns = [
    path('', index, name='index'), # Maintenant, `index` gère aussi la recherche/filtrage
    path('tutoriels/<int:dist_id>/', tutoriels, name='tutoriels'),
    path('distribution/<int:id>/', distribution_detail, name='distribution_detail'),
    # path('rechercher/', rechercher_distribution, name='rechercher_distribution'), # Cette ligne est commentée car index la remplace
    path('quiz/', quiz_recommandation, name='quiz_recommandation'), # Nouvelle URL pour le quizz
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.a_propos, name='a_propos'),
]