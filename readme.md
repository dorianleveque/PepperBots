# PepperBots

# 📝 Description of the project

Projet realisé en IML (Interactive Machine Learning). 
Ce projet consistait à créer une application avec QiBullet (simulateur de robot Pepper et Nao) en intégrant du machine learning et des interactions homme / machine

# Objectif

L'objectif était de pouvoir intéragir avec le robot en utilisant différent moyen. On a souhaité interagir avec celui-ci en mettant en place un système de discution dans la console. On peut discuter avec lui, dire bonjour, demander une blague ou plus intéressant, lui donner des taches à faire.

Parmi les taches disponibles, vous pouvez lui demander de:
* regarder au coordonnée x z
* se rendre au coordonnée x z
* chercher un objet dans la scene qu'il a apprit au préalable (canard ou balle)
* suivre un objet dans la scene qu'il a apprit au préalable (canard ou balle)

Lorsqu'il suit un objet, il est possible de déplacer avec son curseur l'objet dans la scene. Pepper essayera de le suivre tant qu'il reste dans son champ de vision.

# Fonctionnement
Il y a deux réseaux de neurones qui ont été implémenté dans le système. Un pour la reconnaissance d'image (Perception) et l'autre pour le tchatbot (Communication).

Le dataset de la reconnaissance d'image à été généré à l'aide de qiBullet. On a tenté d'extraire des coordonnées pour géné afin d'entrainer notre modèle 

# 📜 Execution

Plusieurs commandes sont disponibles dans le projet:

* python main.py : lance le projet
* python train perception -g: lance la génération du dataset puis l'apprentissage du model de perception
* python train communication: lance l'apprentissage du model de communication  