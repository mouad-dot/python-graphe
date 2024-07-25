# Générateur de PDF à partir de fichiers CSV

Ce projet permet de générer des rapports PDF à partir de fichiers CSV contenant des informations sur les appels effectués. Le script permet de filtrer les données par email, description, date ou nom de famille et de générer des graphiques et des tableaux récapitulatifs.

## Prérequis

Assurez-vous d'avoir Python 3 installé sur votre machine. Vous pouvez télécharger Python à partir de [python.org](https://www.python.org/).

Installez les bibliothèques nécessaires en utilisant pip :

```bash
pip install matplotlib pandas tk

Sur certaines distributions Linux, vous pourriez avoir besoin d'installer tkinter séparément :

sudo apt-get install python3-tk

Utilisation
1-Téléchargez le projet :

Clonez le dépôt ou téléchargez les fichiers nécessaires.

2-Installez les dépendances :

Assurez-vous d'avoir installé toutes les dépendances nécessaires en utilisant le fichier 'requirements.txt' :

pip install -r requirements.txt

3-Exécutez le script principal :

Lancez le script script.py :

python script.py

4-Utilisez l'interface utilisateur :

Une fenêtre s'ouvrira, vous permettant de sélectionner un fichier CSV, de choisir une méthode de filtre et d'entrer une valeur de filtre.
Cliquez sur le bouton "Sélectionner le fichier CSV" pour choisir le fichier à traiter.
Cliquez sur le bouton "Générer le PDF" pour générer le rapport.
Description des fonctionnalités
Lecture de Fichiers CSV
Le script lit le fichier CSV sélectionné par l'utilisateur et vérifie que les colonnes nécessaires sont présentes. Il peut également filtrer les données par email si nécessaire.

Génération des Données pour les Tableaux
Le script génère des données pour plusieurs tableaux en fonction des filtres sélectionnés :

Description : Filtre par description et génère un tableau récapitulatif des appels.
Nom de famille : Filtre par nom de famille et génère un tableau récapitulatif des appels.
Date : Filtre par date et génère un tableau récapitulatif des appels.
Tracé des Graphiques
Le script génère des graphiques à partir des données filtrées :

Tableau 2 : Affiche les appels totaux par description.
Tableau 3 : Affiche les appels totaux par jour.
Tableau 4 : Affiche les appels totaux par jour pour les segments professionnels.
Génération du PDF
Le script génère un fichier PDF contenant les graphiques et tableaux récapitulatifs. Si un filtre par email est appliqué, un graphique en secteur montrant la distribution des emails est également inclus.


Ce fichier `README.md` inclut toutes les informations nécessaires pour installer et utiliser le script, ainsi que le code complet du script.


