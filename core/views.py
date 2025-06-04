from django.shortcuts import render, get_object_or_404
from .models import Distribution, Tutoriel

# Create your views here.

def index(request):
    distributions = Distribution.objects.all()
    return render(request, 'core/index.html', {'distributions': distributions})

def tutoriels(request, dist_id):
    tutoriels = Tutoriel.objects.filter(Distribution__id=dist_id)
    return render(request, 'core/tutoriels.html', {'tutoriels': tutoriels})

def distribution_detail(request, id):
    distribution = get_object_or_404(Distribution, id=id)
    tutoriels = distribution.tutoriels.all()
    return render(request, 'core/distribution_detail.html', {
        'distribution': distribution,
        'tutoriels': tutoriels
    })
