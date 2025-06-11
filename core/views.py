# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q # Import Q pour les requêtes complexes
from .models import Distribution, Tutoriel
from .forms import DistributionFilterForm, QuizForm # Importez les nouveaux formulaires
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ComparaisonForm

# --- Vue pour la liste des distributions avec filtrage avancé ---
def index(request):
    # Initialise le formulaire de filtre avec les données GET si présentes
    form = DistributionFilterForm(request.GET)
    distributions = Distribution.objects.all()

    # Applique les filtres si le formulaire est valide et que des filtres sont renseignés
    if form.is_valid():
        query = form.cleaned_data.get('q')
        niveau_experience = form.cleaned_data.get('niveau_experience')
        usage_principal = form.cleaned_data.get('usage_principal')
        environnement_bureau = form.cleaned_data.get('environnement_bureau')
        modele_publication = form.cleaned_data.get('modele_publication')
        categorie = form.cleaned_data.get('categorie')
        ressources_requises = form.cleaned_data.get('ressources_requises')


        if query:
            distributions = distributions.filter(
                Q(nom__icontains=query) | Q(description__icontains=query)
            )
        if niveau_experience:
            distributions = distributions.filter(niveau_experience=niveau_experience)
        if usage_principal:
            distributions = distributions.filter(usage_principal=usage_principal)
        if environnement_bureau:
            distributions = distributions.filter(environnement_bureau=environnement_bureau)
        if modele_publication:
            distributions = distributions.filter(modele_publication=modele_publication)
        if categorie:
            distributions = distributions.filter(categorie=categorie)
        if ressources_requises:
            distributions = distributions.filter(ressources_requises=ressources_requises)


    # Pagination (comme dans votre recherche actuelle, mais appliquée aux résultats filtrés)
    paginator = Paginator(distributions, 9) # Ex: 9 distributions par page pour la grille
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/index.html', {
        'distributions': page_obj, # On envoie l'objet paginé
        'form': form, # Passe le formulaire au template
    })

# --- Vue pour le Quizz de Recommandation ---
def quiz_recommandation(request):
    recommended_distros = []
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            # Récupère les réponses du quizz
            q1_experience = form.cleaned_data['q1_experience']
            q2_usage = form.cleaned_data['q2_usage']
            q3_desktop = form.cleaned_data['q3_desktop']
            q4_updates = form.cleaned_data['q4_updates']
            q5_hardware = form.cleaned_data['q5_hardware']

            # Logique de matching : trouvez les distributions qui correspondent aux critères
            # Cette logique peut être plus complexe et attribuer des scores
            # Pour commencer, faisons une correspondance directe
            matching_distros = Distribution.objects.all()

            if q1_experience:
                matching_distros = matching_distros.filter(niveau_experience=q1_experience)
            if q2_usage:
                matching_distros = matching_distros.filter(usage_principal=q2_usage)
            if q3_desktop:
                # Ici, vous pouvez avoir une logique plus fine. Ex: si l'utilisateur veut "léger",
                # match contre Xfce, LXQt. Pour l'instant, match direct.
                matching_distros = matching_distros.filter(environnement_bureau=q3_desktop)
            if q4_updates:
                matching_distros = matching_distros.filter(modele_publication=q4_updates)
            if q5_hardware:
                matching_distros = matching_distros.filter(ressources_requises=q5_hardware)

            # Si aucune distribution ne correspond parfaitement, élargissez la recherche
            if not matching_distros.exists():
                # Exemple : on prend les plus populaires pour l'expérience et l'usage
                messages.info(request, "Nous n'avons pas trouvé de correspondance exacte, voici quelques distributions populaires qui pourraient vous convenir.")
                recommended_distros = Distribution.objects.filter(
                    Q(niveau_experience='débutant') | Q(usage_principal='bureau')
                ).distinct()[:3] # Limite à 3 suggestions
            else:
                recommended_distros = matching_distros.distinct()[:5] # Limite à 5 recommandations

            return render(request, 'core/quiz_results.html', {
                'recommended_distros': recommended_distros,
                'form': form, # Passe le formulaire avec les réponses pour l'affichage
            })
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire du quizz.")
    else:
        form = QuizForm() # Formulaire vide pour la première visite

    return render(request, 'core/quiz.html', {'form': form})


# --- Vos autres vues restent inchangées ---
# Page d'accueil (maintenant modifiée pour inclure les filtres)
# def index(request): # Remplacée par la nouvelle version ci-dessus
#     distributions = Distribution.objects.all()
#     return render(request, 'core/index.html', {'distributions': distributions})

# Liste des tutoriels d'une distribution
def tutoriels(request, dist_id):
    tutoriels = Tutoriel.objects.filter(distribution__id=dist_id)
    return render(request, 'core/tutoriels.html', {'tutoriels': tutoriels})

# Détail d'une distribution (modifié pour afficher les nouvelles infos de DL)
def distribution_detail(request, id):
    distribution = get_object_or_404(Distribution, id=id)
    tutoriels = distribution.tutoriels.all()
    return render(request, 'core/distribution_detail.html', {
        'distribution': distribution,
        'tutoriels': tutoriels
    })

# La recherche est maintenant intégrée dans la vue `index`
# def rechercher_distribution(request): # Cette vue n'est plus nécessaire si 'index' gère tout
#     query = request.GET.get('q', '')
#     distributions_list = Distribution.objects.filter(nom__icontains=query) if query else []
#
#     # Ajout de la pagination
#     paginator = Paginator(distributions_list, 5)  # 5 distributions par page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'core/rechercher.html', {
#         'query': query,
#         'distributions': page_obj,  # On envoie l'objet paginé
#     })

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


def comparer_distributions(request):
    distributions_a_comparer = []
    if request.method == 'POST':
        form = ComparaisonForm(request.POST)
        if form.is_valid():
            # Récupérer les IDs des distributions sélectionnées
            dist_id1 = form.cleaned_data['distribution1'].id
            dist_id2 = form.cleaned_data['distribution2'].id
            dist_id3 = form.cleaned_data['distribution3'].id if form.cleaned_data['distribution3'] else None

            # Récupérer les objets Distribution correspondant aux IDs
            # Utilisation de Q pour éviter les doublons dans les IDs si l'utilisateur sélectionne la même distribution plusieurs fois
            q_objects = Q(pk=dist_id1) | Q(pk=dist_id2)
            if dist_id3:
                q_objects |= Q(pk=dist_id3)

            distributions_a_comparer = Distribution.objects.filter(q_objects).distinct()

            # S'assurer qu'il y a au moins 2 distributions uniques
            if len(distributions_a_comparer) < 2:
                # Gérer le cas où moins de 2 distributions uniques ont été sélectionnées
                # Par exemple, ajouter un message d'erreur au formulaire ou rediriger
                form.add_error(None, "Veuillez sélectionner au moins deux distributions différentes pour la comparaison.")
                distributions_a_comparer = [] # Vider la liste pour ne pas afficher de comparaison incomplète
        else:
            # Le formulaire n'est pas valide (e.g., champs requis non remplis)
            pass # Les erreurs du formulaire seront affichées automatiquement dans le template
    else:
        form = ComparaisonForm()

    context = {
        'form': form,
        'distributions_a_comparer': distributions_a_comparer,
    }
    return render(request, 'core/comparer_distributions.html', context)

