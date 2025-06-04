from django.urls import path
from .views import index, tutoriels, distribution_detail

urlpatterns = [
    path('', index, name='index'),
    path('tutoriels/<int:dist_id>/', tutoriels, name='tutoriels'),
    path('distribution/<int:id>/', distribution_detail, name='distribution_detail'),
]
