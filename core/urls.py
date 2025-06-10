from django.urls import path
from .views import index, tutoriels, distribution_detail, rechercher_distribution
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('tutoriels/<int:dist_id>/', tutoriels, name='tutoriels'),
    path('distribution/<int:id>/', distribution_detail, name='distribution_detail'),
    path('rechercher/', rechercher_distribution, name='rechercher_distribution'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.a_propos, name='a_propos'),
]
