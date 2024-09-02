# Trombino
Génération de trombinoscope en pdf automatique, à partir d'une liste et d'un ensemble de photos.

* auteur: Sebastien Kramm
* statut: stabilisé en v1 (2022-09-03)
* home page: https://github.com/skramm/trombino
* licence: [WTFPL](https://en.wikipedia.org/wiki/WTFPL)

Calibré pour des groupes de 3-16..20 personnes par page, pour une année d'une promo de type universitaire (20-100 ou plus personnes, réparties en plusieurs groupes).


## Exemple de résultat (réel)

![exemple](trombi_1_800.jpg)


## Outils nécessaires
* bash (incluant le calculateur `bc`)
* LaTeX, avec le package `tabularx`

## Installation

Il est possible d'utiliser le programme directement depuis le dépot cloné.
Mais il est préférable de l'installer sur la machine, via:
```
$ sudo ./install
```
Ceci va copier le script dans `/usr/local/bin/` et le fichier de configuration (fichier d'en-tête LaTeX) dans `/etc/trombino/`.

## Utilisation

Il faut avoir une liste des personnes, et prendre une photo par personne, **dans l'ordre de la liste**.
En cas d'absence, il faut prendre une photo "vide", pour conserver l'ordre.

Ensuite, un petit traitement batch des photos est probablement nécessaire (recadrage, augmentation de la luminosité, conversion en N&B, etc).
Ceci se fait facilement avec des outils comme [Imagemagik](https://imagemagick.org/).
Dans l'idéal, il faudrait avoir des photos de quelques dizaines de ko.

Le script va générer deux fichiers pdf:

* `trombi_global.pdf`: trombinoscope global, sur plusieurs pages;
* `trombi_groupes.pdf`: trombinoscope avec une page par groupe, avec les étudiants faisant partie de ce groupe.

### Données d'entrées du script

* une liste en CSV contenant sur 3 champs:
Groupe, Nom, Prénom <br>
A coller dans le dossier racine. Les lignes vides seront ignorées.
* copier dans le dossier `photos` les photos, dans l'ordre de la liste.

Attention, il doit y avoir autant de photos que de lignes dans le fichier d'entrée!

L'exécution se fait dans un terminal ouvert dans le dossier où se trouve le fichier-liste et le dossier des photos:
```
$ trombino
```

On peut avoir les options disponibles avec:
```
$ trombino -h
```
(voir ci-dessous).


### Paramétrage
* éditer le fichier `entete_ecole.txt` et y mettre le nom de l'établissement, de la promo, etc.
Sera imprimé dans l'en-tête de gauche.
* éditer le fichier `entete_annee.txt` et y mettre l'année en cours (ou ce que vous voulez d'autre!).
Sera imprimé dans l'en-tête de droite.

### Syntaxe d'appel

Des valeurs par défaut sont prévues, mais on peut passer des options pour les modifier.

`$ trombino [-hs] [-l fichier_liste] [-p dossier_photos] [-o nom_pdf] [-c nb_cols]`

* `-l`: pour spécifier un autre nom du fichier csv d'entrée (liste des étudiants)
* `-p`: pour indiquer un autre dossier pour les photos
* `-o`: pour donner un autre nom au fichier pdf généré (sans extension!!)
<br>Par exemple, `-o aaa` produira les deux fichiers `aaa_global.pdf` et `aaa_groupes.pdf`
* `-c`: pour modifier le nombre de colonnes. La taille des photos est automatiquement ajustée.
* `-s`: permute nom - prénom
* `-h`: affiche cette aide
* `-d`: active le mode "debug", ce qui imprimera le nom du fichier de la photo avec la photo
(utile en cas d'erreur nom/photo)

 
## Exemple/demo

Des données de démo dont incluses, vous pouvez tester directement.
Il y a:

* une liste de noms (thx: https://fossbytes.com/tools/random-name-generator)
* une liste de "photos" (thx: https://multiavatar.com/).
Ces avatars sont générés via le script `gen_avatars.sh` (requires Imagemagick)

Tapez la commande suivante dans le dossier racine, une fois le repo cloné:
```
$ ./trombino
```
Ceci doit vous donner dans un fichier `trombi.pdf`, similaire à celui qui est fourni (`trombi_exemple.pdf`).

Vous pouvez aussi essayer ceci pour voir les mêmes données en 5 colonnes:
```
$ ./trombino -c 5
```

## Extension optionnelle: auto-cropping

L'un des points faible de ce programme est le fait qu'il nécessite en pratique un "cropping" des photos.
En effet, en général le cadrage fait qu'il est peu pratique d'avoir dès la prise de vue un cadrage type "photo d'identité".
Le cropping peut se faire à la main, photo par photo, à l'aide d'un outil ad hoc, mais c'est évidemment fastidieux (et donc, non).
On peut aussi l'automatiser via un script (utilisant par exemple [imagemagick](https://imagemagick.org/)) qui prend chaque photo et lui applique un cropping fixe, mais il faut alors prédeterminer la bonne "bounding box", ce qui prend du temps.
Sans compter que on aura toujours des étudiants qui sont un peu trop à gauche, à droite, et donc le cropping identique pour toutes les photos va générer soit des "coupages de têtes", soit des images un peu trop "larges".

Depuis 2024/09, une extension utilisant la bibliothèque OpenCv est incluse et permet d'avoir un **cropping automatique**, par une détection de visage dans la photo.
Il faut donc avoir Opencv installé localement, mais il semble que ceci soit assez facile, via:
```
$ pip install opencv-python
```
Ceci a été testé avec la version 4.5.5, mais devrait aussi fonctionner avec des versions 3.

L'utilisation de fait via l'appel du programme `autocrop`, qui prend deux arguments.
Le premier est le nom du dossier dans lequel se trouve les photos brutes.
Le second est le nom du dossier dans lequel seront placés les images "croppées"
(sera crée s'il n'existe pas).

Par exemple:
```
$ autocrop src dst
```

Ce script bash lance pour chaque photo le programme Python `trombino_autocrop_gui.py`
qui va lancer une cascade de classifieurs pour tenter de trouver un visage
(voir
https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html
pour des détails), avec des valeurs de paramètres par défaut.
Si les paramètres par défaut ne trouvent pas de visage, alors une interface graphique est démarrée
(basée sur le module "HighGui" de OpenCV).
Des sliders permettent d'ajuster les paramètres, le plus important étant l'échelle ("scale").
Une fois un visage trouvé, il faut alors appuyer sur "espace" pour sauvegarder l'image "croppée".

Dans le cas où il s'agit d'une photo "vide", un appui sur ESC va sauvegarder la photo telle quelle.


