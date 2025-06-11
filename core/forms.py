from django import forms
from .models import (
    Distribution, # N'oubliez pas d'importer le modèle Distribution
    EXPERIENCE_CHOICES, USAGE_CHOICES, DESKTOP_ENV_CHOICES,
    RELEASE_MODEL_CHOICES, CATEGORIE_CHOICES # Importez tous les CHOICES
)

# --- Formulaire de Comparaison de Distributions ---
class ComparaisonForm(forms.Form):
    # Permet de sélectionner jusqu'à 3 distributions pour la comparaison.
    distribution1 = forms.ModelChoiceField(
        queryset=Distribution.objects.all().order_by('nom'),
        label="Distribution 1",
        empty_label="Sélectionnez une distribution",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap pour la liste déroulante
    )
    distribution2 = forms.ModelChoiceField(
        queryset=Distribution.objects.all().order_by('nom'),
        label="Distribution 2",
        empty_label="Sélectionnez une distribution",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )
    distribution3 = forms.ModelChoiceField(
        queryset=Distribution.objects.all().order_by('nom'),
        label="Distribution 3 (optionnel)",
        empty_label="Sélectionnez une distribution",
        required=False, # Ce champ est optionnel
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )

# --- Formulaire de Filtrage Avancé ---
class DistributionFilterForm(forms.Form):
    # Champ de recherche texte
    q = forms.CharField(
        label='Rechercher',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nom de la distribution...', 'class': 'form-control'}), # Style Bootstrap
    )

    # Filtres basés sur les choix des modèles
    niveau_experience = forms.ChoiceField(
        choices=[('', 'Tous les niveaux')] + list(EXPERIENCE_CHOICES),
        required=False,
        label="Niveau d'expérience",
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )
    usage_principal = forms.ChoiceField(
        choices=[('', 'Tous les usages')] + list(USAGE_CHOICES),
        required=False,
        label="Usage principal",
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )
    environnement_bureau = forms.ChoiceField(
        choices=[('', 'Tous les environnements')] + list(DESKTOP_ENV_CHOICES),
        required=False,
        label="Environnement de bureau",
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )
    modele_publication = forms.ChoiceField(
        choices=[('', 'Tous les modèles')] + list(RELEASE_MODEL_CHOICES),
        required=False,
        label="Modèle de publication",
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )
    categorie = forms.ChoiceField(
        choices=[('', 'Toutes les catégories')] + list(CATEGORIE_CHOICES),
        required=False,
        label="Catégorie de base",
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )
    ressources_requises = forms.ChoiceField(
        choices=[('', 'Toutes les ressources')] + [
            ("faibles", "Faibles"),
            ("moyennes", "Moyennes"),
            ("elevees", "Élevées")
        ],
        required=False,
        label="Ressources matérielles",
        widget=forms.Select(attrs={'class': 'form-select'}) # Style Bootstrap
    )

    # Note: Vous pouvez décommenter et utiliser MultipleChoiceField avec CheckboxSelectMultiple
    # si vous souhaitez permettre la sélection de plusieurs usages ou environnements.

# --- Formulaire du Quizz de Recommandation ---
class QuizForm(forms.Form):
    q1_experience = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        label="Quel est votre niveau d'expérience avec Linux ?",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}) # Style Bootstrap pour les radios
    )
    q2_usage = forms.ChoiceField(
        choices=USAGE_CHOICES,
        label="Quel sera l'usage principal de votre système ?",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}) # Style Bootstrap
    )
    q3_desktop = forms.ChoiceField(
        choices=DESKTOP_ENV_CHOICES,
        label="Préférez-vous un environnement de bureau léger, moderne, ou personnalisable ?",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}) # Style Bootstrap
    )
    q4_updates = forms.ChoiceField(
        choices=RELEASE_MODEL_CHOICES,
        label="Préférez-vous la stabilité (mises à jour moins fréquentes) ou les dernières nouveautés (mises à jour continues) ?",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}) # Style Bootstrap
    )
    q5_hardware = forms.ChoiceField(
        choices=[
            ("faibles", "Mon PC est ancien ou a peu de ressources"),
            ("moyennes", "Mon PC est de gamme moyenne"),
            ("elevees", "Mon PC est puissant / récent")
        ],
        label="Quelles sont les ressources matérielles de votre PC ?",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}) # Style Bootstrap
    )