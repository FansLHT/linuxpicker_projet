from django.shortcuts import render, get_object_or_404
from .models import Distribution, Tutoriel

# Page d'accueil
def index(request):
    distributions = Distribution.objects.all()
    return render(request, 'core/index.html', {'distributions': distributions})

# Liste des tutoriels d'une distribution
def tutoriels(request, dist_id):
    tutoriels = Tutoriel.objects.filter(Distribution__id=dist_id)
    return render(request, 'core/tutoriels.html', {'tutoriels': tutoriels})

# Détail d'une distribution
def distribution_detail(request, id):
    distribution = get_object_or_404(Distribution, id=id)
    tutoriels = distribution.tutoriels.all()
    return render(request, 'core/distribution_detail.html', {
        'distribution': distribution,
        'tutoriels': tutoriels
    })

# ✅ Fonction pour rechercher une distribution par nom
def rechercher_distribution(request):
    query = request.GET.get('q', '')  # récupération du mot-clé de recherche
    distributions = Distribution.objects.filter(nom__icontains=query) if query else []
    return render(request, 'core/rechercher.html', {
        'query': query,
        'distributions': distributions
    })
