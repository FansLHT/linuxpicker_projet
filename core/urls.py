from django.urls import path
from .views import index, tutoriels

urlpatterns = [
    path('', index, name='index'),
    path('tutoriels/<int:dist_id>/', tutoriels, name='tutoriels'),
]
