# LinuxPicker : Trouvez Votre Distribution Linux Idéale !

## Description du Projet

LinuxPicker est une application web conviviale conçue pour aider les utilisateurs, qu'ils soient novices ou expérimentés, à choisir la distribution Linux qui correspond le mieux à leurs besoins et préférences. Grâce à un quiz interactif et une base de données détaillée, LinuxPicker simplifie le processus de découverte et de comparaison des distributions Linux.

## Fonctionnalités Clés

* **Quiz Interactif :** Un questionnaire simple pour guider les utilisateurs vers les distributions les plus adaptées.
* **Base de Données de Distributions :** Accès à une liste complète de distributions Linux avec des informations détaillées (description, environnement de bureau, facilité d'utilisation, communauté, etc.).
* **Page de Détails de Distribution :** Informations approfondies pour chaque distribution, y compris les avantages, les inconvénients et des tutoriels associés.
* **Comparateur de Distributions :** Permet aux utilisateurs de comparer plusieurs distributions côte à côte pour une meilleure prise de décision.
* **Section Tutoriels :** Une collection de tutoriels couvrant divers aspects de Linux, allant de l'installation à des conseils d'utilisation avancés.
* **Tableau de Bord Administratif :** Un panneau d'administration pour gérer les distributions, les questions du quiz, les tutoriels, etc. (Accès via `/admin/`).

## Technologies Utilisées

* **Backend :** Python 3.12, Django 5.2.1
* **Frontend :** HTML5, CSS3, JavaScript
* **Framework CSS :** Bootstrap 5.3.3
* **Base de Données :** SQLite3 (par défaut en développement), PostgreSQL (recommandé pour la production)
* **Icônes :** Font Awesome 6
* **Gestion de Projet :** Git

## Installation et Lancement (pour les développeurs)

Suivez ces étapes pour configurer et lancer le projet LinuxPicker sur votre machine locale.

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/VotreNomUtilisateur/linuxpicker_projet.git](https://github.com/VotreNomUtilisateur/linuxpicker_projet.git)
    cd linuxpicker_projet
    ```
    *(Remplacez `VotreNomUtilisateur` par votre nom d'utilisateur GitHub/GitLab)*

2.  **Créer et activer un environnement virtuel :**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Installer les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration de la base de données :**
    Par défaut, Django utilise SQLite. Aucune configuration supplémentaire n'est nécessaire pour le développement.
    Si vous souhaitez utiliser PostgreSQL, configurez les paramètres dans `linuxpicker_projet/settings.py`.

5.  **Exécuter les migrations de base de données :**
    ```bash
    python manage.py migrate
    ```

6.  **Créer un superutilisateur (pour accéder au panneau d'administration) :**
    ```bash
    python manage.py createsuperuser
    ```
    Suivez les instructions pour créer votre compte administrateur.

7.  **Lancer le serveur de développement :**
    ```bash
    python manage.py runserver
    ```
    L'application sera accessible à l'adresse : `http://127.0.0.1:8000/`

## Exécution des Tests

Pour exécuter les tests unitaires du projet :

```bash
python manage.py test