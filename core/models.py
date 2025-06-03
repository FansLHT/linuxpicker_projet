from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Distribution(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    descriptiion = models.TextField()
    site_officiel = models.URLField()
    image = models.ImageField(upload_to='distributions/')

    def __str__(self):
        return self.nom


class Tutoriel(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    Distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='tutoriels')
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titre
