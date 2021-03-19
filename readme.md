<div align="center">
    <img src="assets/pepperBots-logo.jpg" alt="drawing" width="200px;"/>
    <h1>
        <b>
          PepperBots
        </b>
    </h1>
    <h3>Pepper robot will tried to satisty your desire</h3>
    </br>
    </br>
</div>

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
Pour l'instant pepper ne détecte pas les obstacles pour les éviter, mais ce serait à ajouter. 
De plus il faudrait ajouter plus d'objet dans la scène. On s'est contenté de deux puisqu'on avait et on a encore des erreurs de détection. Elle confond parfois la balle avec le canard, ou n'arrive pas à détecter la balle.

# 📜 Execution

Plusieurs commandes sont disponibles dans le projet:

* python main.py : lance le projet
* python train perception -g: lance la génération du dataset puis l'apprentissage du modèle de perception
* python train communication: lance l'apprentissage du modèle de communication  