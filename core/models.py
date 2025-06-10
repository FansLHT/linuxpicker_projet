# core/models.py

from django.db import models
from django.contrib.auth.models import User

# --- Nouvelles listes de choix pour les filtres ---
# Niveau d'expérience
EXPERIENCE_CHOICES = [
    ("débutant", "Débutant"),
    ("intermédiaire", "Intermédiaire"),
    ("expert", "Expert"),
]

# Type d'utilisation
USAGE_CHOICES = [
    ("bureau", "Bureau (usage quotidien)"),
    ("serveur", "Serveur"),
    ("gaming", "Gaming"),
    ("sécurité", "Sécurité / Pentesting"),
    ("dev", "Développement"),
    ("ancien_pc", "Ancien PC / Faibles ressources"),
    ("embarque", "Système Embarqué"),
    ("multimedia", "Multimédia"),
]

# Environnement de Bureau
DESKTOP_ENV_CHOICES = [
    ("gnome", "GNOME"),
    ("kde", "KDE Plasma"),
    ("xfce", "Xfce"),
    ("cinnamon", "Cinnamon"),
    ("mate", "MATE"),
    ("lxqt", "LXQt"),
    ("autre", "Autre / Minimaliste"),
]

# Modèle de publication (Release Model)
RELEASE_MODEL_CHOICES = [
    ("stable", "Stable (Mises à jour par version)"),
    ("rolling", "Rolling Release (Mises à jour continues)"),
]

# Base de la distribution (votre champ existant, mais avec plus de granularité si nécessaire)
# J'ai ajouté plus de choix ici pour l'exemple.
CATEGORIE_CHOICES = [
    ("Debian", "Debian-based"),
    ("Ubuntu", "Ubuntu-based"), # Souvent considérée comme une catégorie à part
    ("Arch", "Arch-based"),
    ("RedHat", "Red Hat / Fedora / CentOS-based"),
    ("Suse", "OpenSUSE / SUSE-based"),
    ("Autre", "Indépendante / Autre"),
]

# --- Modifications du modèle Distribution ---
class Distribution(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField() # Correction de la faute de frappe ici
    site_officiel = models.URLField(blank=True)
    image = models.ImageField(upload_to='distributions/')

    # Ancien champ 'categorie', mis à jour avec plus de choix
    categorie = models.CharField(
        max_length=100,
        choices=CATEGORIE_CHOICES,
        default="Autre" # Assurez-vous que le default est un choix valide
    )

    # Nouveaux champs pour le filtrage avancé et le quizz
    niveau_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="débutant",
        verbose_name="Niveau d'expérience recommandé"
    )
    usage_principal = models.CharField(
        max_length=50,
        choices=USAGE_CHOICES,
        default="bureau",
        verbose_name="Usage principal"
    )
    environnement_bureau = models.CharField(
        max_length=50,
        choices=DESKTOP_ENV_CHOICES,
        default="gnome",
        verbose_name="Environnement de bureau par défaut"
    )
    modele_publication = models.CharField(
        max_length=20,
        choices=RELEASE_MODEL_CHOICES,
        default="stable",
        verbose_name="Modèle de publication"
    )
    # Champ pour les ressources matérielles (peut être plus précis que juste "ancien_pc" dans l'usage)
    ressources_requises = models.CharField(
        max_length=20,
        choices=[
            ("faibles", "Faibles (vieux PC)"),
            ("moyennes", "Moyennes"),
            ("elevees", "Élevées (hautes performances)")
        ],
        default="moyennes",
        verbose_name="Ressources matérielles requises"
    )
    # Optionnel: liens de téléchargement spécifiques, sommes de contrôle
    lien_telechargement_direct = models.URLField(blank=True, verbose_name="Lien de téléchargement direct (.iso)")
    lien_telechargement_torrent = models.URLField(blank=True, verbose_name="Lien Torrent / Magnet")
    checksum_sha256 = models.CharField(max_length=64, blank=True, verbose_name="SHA256 Checksum")


    class Meta:
        verbose_name = "Distribution Linux"
        verbose_name_plural = "Distributions Linux"

    def __str__(self):
        return self.nom
        

class Tutoriel(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    Distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='tutoriels')
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Tutoriel"
        verbose_name_plural = "Tutoriels"

    def __str__(self):
        return self.titre

