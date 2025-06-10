from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Distribution, Tutoriel
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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

def a_propos(request):
    """Vue pour la page À propos"""
    return render(request, 'core/a_propos.html')

def contact(request):
    """Vue pour la page Contact"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        
        if nom and email and sujet and message:
            try:
                # Envoyer l'email (optionnel - nécessite configuration SMTP)
                send_mail(
                    subject=f'Contact LinuxPicker: {sujet}',
                    message=f'De: {nom} ({email})\n\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['ralaiarimananjara@gmail.com'],  # Remplacez par votre email
                    fail_silently=False,
                )
                messages.success(request, 'Votre message a été envoyé avec succès!')
            except Exception as e:
                messages.success(request, 'Votre message a été reçu! Nous vous répondrons bientôt.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    return render(request, 'core/contact.html')