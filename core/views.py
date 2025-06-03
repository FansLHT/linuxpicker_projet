from django.shortcuts import render
from .models import Distribution, Tutoriel

# Create your views here.

def index(request):
    distributions = Distribution.objects.all()
    return render(request, 'core/index.html', {'distributions': distributions})

def tutoriels(request, dist_id):
    tutoriels = Tutoriel.objects.filter(Distribution__id=dist_id)
    return render(request, 'core/tutoriels.html', {'tutoriels': tutoriels})
