# core/forms.py
from django import forms
from .models import (
    EXPERIENCE_CHOICES, USAGE_CHOICES, DESKTOP_ENV_CHOICES,
    RELEASE_MODEL_CHOICES, CATEGORIE_CHOICES # Importez tous les CHOICES
)

# --- Formulaire de Filtrage Avancé ---
class DistributionFilterForm(forms.Form):
    # Champ de recherche texte (comme votre recherche actuelle)
    q = forms.CharField(
        label='Rechercher',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nom de la distribution...'}),
    )

    # Filtres basés sur les choix des modèles
    niveau_experience = forms.ChoiceField(
        choices=[('', 'Tous les niveaux')] + list(EXPERIENCE_CHOICES),
        required=False,
        label="Niveau d'expérience",
    )
    usage_principal = forms.ChoiceField(
        choices=[('', 'Tous les usages')] + list(USAGE_CHOICES),
        required=False,
        label="Usage principal",
    )
    environnement_bureau = forms.ChoiceField(
        choices=[('', 'Tous les environnements')] + list(DESKTOP_ENV_CHOICES),
        required=False,
        label="Environnement de bureau",
    )
    modele_publication = forms.ChoiceField(
        choices=[('', 'Tous les modèles')] + list(RELEASE_MODEL_CHOICES),
        required=False,
        label="Modèle de publication",
    )
    categorie = forms.ChoiceField( # Utilise votre champ 'categorie' existant
        choices=[('', 'Toutes les catégories')] + list(CATEGORIE_CHOICES),
        required=False,
        label="Catégorie de base",
    )
    ressources_requises = forms.ChoiceField(
        choices=[('', 'Toutes les ressources')] + [
            ("faibles", "Faibles"), # Utilisez les valeurs exactes des choices du modèle
            ("moyennes", "Moyennes"),
            ("elevees", "Élevées")
        ],
        required=False,
        label="Ressources matérielles",
    )

    # Note: Vous pouvez ajouter des champs de type CheckboxSelectMultiple pour permettre la sélection multiple
    # Exemple pour les usages :
    # usage_principal = forms.MultipleChoiceField(
    #     choices=USAGE_CHOICES,
    #     required=False,
    #     label="Usages principaux",
    #     widget=forms.CheckboxSelectMultiple,
    # )


# --- Formulaire du Quizz de Recommandation ---
# Ce formulaire sera probablement plus simple, avec des questions directes.
# Les réponses serviront à "matcher" les distributions.
class QuizForm(forms.Form):
    q1_experience = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        label="Quel est votre niveau d'expérience avec Linux ?",
        widget=forms.RadioSelect, # RadioSelect pour une seule sélection
    )
    q2_usage = forms.ChoiceField(
        choices=USAGE_CHOICES,
        label="Quel sera l'usage principal de votre système ?",
        widget=forms.RadioSelect,
    )
    q3_desktop = forms.ChoiceField(
        choices=DESKTOP_ENV_CHOICES,
        label="Préférez-vous un environnement de bureau léger, moderne, ou personnalisable ?",
        widget=forms.RadioSelect,
        # Vous pourriez mapper ces choix à des DE spécifiques en interne
        # Par exemple: Léger -> Xfce, LXQt; Moderne -> GNOME, KDE; Personnalisable -> KDE, GNOME, ou Arch+choix
    )
    q4_updates = forms.ChoiceField(
        choices=RELEASE_MODEL_CHOICES,
        label="Préférez-vous la stabilité (mises à jour moins fréquentes) ou les dernières nouveautés (mises à jour continues) ?",
        widget=forms.RadioSelect,
    )
    q5_hardware = forms.ChoiceField(
        choices=[
            ("faibles", "Mon PC est ancien ou a peu de ressources"),
            ("moyennes", "Mon PC est de gamme moyenne"),
            ("elevees", "Mon PC est puissant / récent")
        ],
        label="Quelles sont les ressources matérielles de votre PC ?",
        widget=forms.RadioSelect,
    )