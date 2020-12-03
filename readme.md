# PepperBots

# 📝 Description of the project

Projet realisé en IML (Interactive Machine Learning). 
Ce projet consistait à créer une application avec QiBullet (simulateur de robot Pepper et Nao) en intégrant du machine learning et des interactions homme / machine

# Objectif

L'objectif était de pouvoir intéragir avec le robot en utilisant différents moyens. On a souhaité interagir avec celui-ci en mettant en place un système de discution dans la console. On peut discuter avec lui, dire bonjour, demander une blague ou plus intéressant, lui donner des taches à faire. Le tout en anglais (of course !). 

Parmi les taches disponibles, vous pouvez lui demander de:
* regarder au coordonnées x z
* se rendre au coordonnées x z
* chercher un objet dans la scene qu'il a appris au préalable (canard ou balle)
* suivre un objet dans la scene qu'il a appris au préalable (canard ou balle)

Lorsqu'il suit un objet, il est possible de déplacer avec son curseur l'objet dans la scene. Pepper essayera de le suivre tant qu'il reste dans son champ de vision.

# Fonctionnement
Il y a deux réseaux de neurones qui ont été implémentés dans le système. Un pour la reconnaissance d'images (Perception) et l'autre pour le chatbot (Communication).

Le dataset de la reconnaissance d'image à été généré à l'aide de qiBullet. On a tenté de faire apprendre au modèle les coordonnées afin de générer des "bounding box" plus facilement et plus efficacement. Cela n'a pas pu etre implémenté malheureusement. Les "bounding box" sont donc calculées en réduisant successivement la fenêtre de detection.

# Prochain objectif
Pour l'instant pepper a du mal à suivre correctement une cible (comme vu en vidéo). Elle gère mal la rotation et donc perd la cible de vue. C'est donc une fonctionalité à affiner. 

# 📜 Execution

Plusieurs commandes sont disponibles dans le projet:

* python main.py : lance le projet
* python train perception -g: lance la génération du dataset puis l'apprentissage du modèle de perception
* python train communication: lance l'apprentissage du modèle de communication  