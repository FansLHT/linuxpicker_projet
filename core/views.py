from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
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

# Recherche avec pagination
def rechercher_distribution(request):
    query = request.GET.get('q', '')
    distributions_list = Distribution.objects.filter(nom__icontains=query) if query else []

    # Ajout de la pagination
    paginator = Paginator(distributions_list, 5)  # 5 distributions par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/rechercher.html', {
        'query': query,
        'distributions': page_obj,  # On envoie l'objet paginé
    })
       