# Discord Bot

## Description

Ce projet est un bot Discord utilisant `discord.py` pour la gestion des commandes et `mysql-connector` pour la connexion avec une base de donnee mysql

## Fonctionnalités
### 1. Ajouter un devoir
**Commande :** `!ajouter_devoir`

Cette commande permet de créer un devoir.

**Paramètres :**
- `matiere` (obligatoire) : La matière du devoir.
- `libelle` (obligatoire) : Le libellé du devoir.
- `date` (obligatoire) : La date d'échéance du devoir au format `j/m/y` (ex : `27/12/2004`).

**Exemple :**
```plaintext
!ajouter_devoir matiere="Test Du Medzik", libelle="Turfu", date=27/12/2004
```

### 2. Mettre à jour un devoir
**Commande** : !mise_a_jour

Met à jour les informations d’un devoir.

**Paramètres :**
- `id` (obligatoire) : L’ID du devoir à mettre à jour.
-	`matiere` (optionnel) : La nouvelle matière du devoir.
- `libelle` (optionnel) : Le nouveau libellé du devoir.
- 	`date` (optionnel) : La nouvelle date d’échéance du devoir au format j/m/y.

**Exemple :**
```plaintext
!mise_a_jour id=1, matiere="Mathématiques", libelle="Devoir d'algèbre"
```

### 3. Lister tous les devoirs
**Commande** : !tous

Liste tous les devoirs enregistrés en base de données.

**Exemple :**
```plaintext
!tous
```

### 4.  Récupérer les devoirs d’une période
**Commande** : !devoir_periode

Récupère les devoirs d’une période donnée.

**Paramètres :**
- `start` (obligatoire) : La date de début au format j/m/y (ex : 27/12/2004).
- `end` (obligatoire) : La date de fin au format j/m/y (ex : 27/12/2004).

**Exemple :**
```plaintext
!devoir_periode start=27/12/2004, end=22/01/2024
```

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :
- Python 3.12
- Un environnement virtuel Python (optionnel mais recommandé)
- Mysql d'installer 

## Installation et configuration

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/JagoOgaj/botDiscordAgenda.git
   cd repository
   ```


2. **Créez un environnement virtuel (optionnel mais recommandé) :**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`
   ```

3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```
    
4. **Configurez les variables d’environnement :**
Assurez-vous de définir les variables d’environnement nécessaires, en créant à la racine le fichier ".env" 
   ```python
    DISCORD_TOKEN=
    DB_NAME=
    DB_HOST=
    DB_USER=
    DB_PWD=
    LOG_LEVEL=
   ```


5. **Configurez la base de donnees :**
Executez la commande "SOURCE path/to/seed/database.sql" afin de creer les tables apres avoir creer la base de donnee
   ```bash
   CREATE DATABASE mon_agenda ;
   USE mon_agenda ;
   SOURCE path/to/seed/database.sql ;
   ```
Assurez vous que la connexion est etablie a l'aide des logs sur le terminal, que le nom plus le mot de passe de l'utilisateur de la base 
de donnees soit correctement renseigner dans le ".env" ainsi que le nom de la base de donnee.

## Lancer le programe

Une fois l'instalation et la configuration terminé pour lancer le bot avec un `python main.py`


