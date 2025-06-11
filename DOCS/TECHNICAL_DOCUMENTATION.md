# Documentation Technique de LinuxPicker

Ce document détaille l'architecture et les choix techniques du projet LinuxPicker.

## 1. Architecture Générale

LinuxPicker est une application web basée sur le framework **Django**. Elle suit l'architecture Model-View-Controller (MVC), bien que Django l'appelle souvent Model-View-Template (MVT).

* **Modèles (Models) :** Définis dans `core/models.py`, ils représentent la structure de la base de données et la logique métier.
* **Vues (Views) :** Définies dans `core/views.py`, elles traitent les requêtes HTTP et renvoient des réponses, interagissant avec les modèles et les templates.
* **Templates (Templates) :** Fichiers HTML situés dans `core/templates/core/`, ils définissent l'interface utilisateur.
* **URLs :** Le routage des requêtes est géré par `linuxpicker/urls.py` (global) et `core/urls.py` (spécifique à l'application `core`).
* **Fichiers Statiques :** CSS, JavaScript, images sont servis depuis `core/static/core/`.

## 2. Modèles de Données (core/models.py)

Voici un aperçu des principaux modèles et de leurs relations.

* **`Distribution`** :
    * `nom (CharField)` : Nom de la distribution (ex: Ubuntu, Fedora).
    * `description (TextField)` : Description complète.
    * `environnement_bureau (CharField)` : Ex: GNOME, KDE Plasma, XFCE.
    * `facilite_utilisation (IntegerField)` : Note de 1 à 5.
    * `communaute (CharField)` : Taille et activité de la communauté.
    * `based_on (CharField)` : Distribution de base (ex: Debian, Arch).
    * `logo (ImageField)` : Logo de la distribution.
    * `# ... autres champs pertinents ...`

* **`Question`** (pour le quiz) :
    * `texte (CharField)` : Le texte de la question.
    * `categorie (CharField)` : Catégorie de la question (ex: "Expérience", "Matériel").
    * `# ... autres champs si besoin (ex: type de question) ...`

* **`Reponse`** (pour le quiz) :
    * `question (ForeignKey à Question)` : La question à laquelle cette réponse se rapporte.
    * `texte (CharField)` : Le texte de la réponse.
    * `valeur (IntegerField)` : Valeur numérique associée à la réponse pour le calcul du score.
    * `# ... d'autres associations si une réponse pointe vers des distributions spécifiques ...`

* **`Tutoriel`** :
    * `titre (CharField)`
    * `contenu (TextField)`
    * `auteur (CharField)`
    * `date_publication (DateTimeField)`
    * `distribution (ForeignKey à Distribution, optionnel)` : Le tutoriel peut être lié à une distribution spécifique.

## 3. Flux des Requêtes

1.  **Requête HTTP :** Un utilisateur accède à une URL (ex: `/quiz/`).
2.  **`linuxpicker/urls.py` :** L'URL globale redirige vers `core/urls.py`.
3.  **`core/urls.py` :** Le chemin est mappé à une fonction de vue (ex: `views.quiz_view`).
4.  **`core/views.py` :**
    * La vue récupère les données nécessaires depuis les modèles (ex: `Question.objects.all()`).
    * Elle traite la logique métier (ex: calcul du score du quiz).
    * Elle prépare le `context` (dictionnaire de données).
    * Elle rend un template (`core/quiz.html`) avec ce `context`.
5.  **`core/templates/core/quiz.html` :** Le template utilise le langage de template de Django pour afficher les données et générer le HTML final.
6.  **Réponse HTTP :** Le HTML généré est renvoyé au navigateur de l'utilisateur.

## 4. Choix Techniques

* **Django :** Choisis pour sa robustesse, sa sécurité intégrée (protection CSRF, XSS), son ORM puissant et son panneau d'administration inclus, ce qui accélère le développement.
* **Bootstrap 5 :** Utilisé pour la réactivité du design et la rapidité du développement frontend grâce à ses composants prédéfinis.
* **Gestion des Statiques :** Django's `staticfiles` est utilisé pour servir CSS, JS et images en développement. Pour la production, un serveur web (Nginx/Apache) serait configuré pour servir ces fichiers directement.
* **Quiz Logic :** Le quiz est basé sur des questions à choix multiples, chaque réponse ayant une "valeur" numérique qui contribue à un score total. Ce score est ensuite utilisé pour recommander des distributions en fonction de seuils ou de correspondances.

## 5. Notes de Développement

* **Environnement Virtuel :** Toujours travailler dans un environnement virtuel pour isoler les dépendances du projet.
* **Migrations :** Ne pas modifier directement la base de données. Utilisez `python manage.py makemigrations` et `python manage.py migrate` pour gérer les changements de schéma.
* **Debug Toolbar :** Pour le développement, installez et utilisez `django-debug-toolbar` pour un meilleur débogage des requêtes SQL, des variables de contexte, etc.
* **Bonnes Pratiques :** Suivre les conventions de nommage de Django, utiliser des vues basées sur des classes pour la complexité, et garder les vues simples en déléguant la logique complexe aux modèles ou à des fonctions utilitaires.