# Trombino
Génération de trombinoscope en pdf automatique, à partir d'une liste et d'un ensemble de photos.

* auteur: Sebastien Kramm
* statut: stabilisé en v1 (2022-09-03)
* home page: https://github.com/skramm/trombino
* licence: [WTFPL](https://en.wikipedia.org/wiki/WTFPL)

Outil en ligne de commande, calibré pour des groupes jusqu'à 20 personnes par page, pour une année d'une promo de type universitaire (20-100 ou plus personnes, réparties en plusieurs groupes).


## 1- Exemple de résultat (réel)

(mais avec des photos anonymisées, pour des raisons évidentes)

![exemple](trombi_1_800.jpg)



## 2 - Installation

## 2.1 - Outils nécessaires
* bash (incluant le calculateur `bc`)
* LaTeX, avec le package `tabularx`
* Python3 & Opencv, pour l'extension de cropping (voir section "Extension")

Tout ceci a été developpé sous Linux/Ubuntu et devrai donc fonctionner sans problème sur des OS basés Linux,
mais ces outils étant assez commun, un usage sous Mac/OSX devrait pouvoir fonctionner également (non-testé!).
Pour ceux travaillant (encore) sous Windows, je vous laisse essayer.


## 2.2 - Téléchargement et installation

Le plus simple consiste à cloner le dépot localement, mais pour ceux peu au fait de l'utilisation de git, une archive d'installation est prévue.

Il est possible d'utiliser le programme directement depuis le dépot cloné, mais il est préférable de l'installer sur la machine, via:
```
$ sudo ./install
```
Ceci va copier les exécutables dans `/usr/local/bin/` et le fichier de configuration (fichier d'en-tête LaTeX) dans `/etc/trombino/`.

## 3 - Utilisation

Il faut avoir une liste des personnes, et prendre une photo par personne, **dans l'ordre de la liste**.
En cas d'absence, il faut prendre une photo "vide", pour conserver l'ordre.

Ensuite, un petit traitement batch des photos peut être réalisé (recadrage, augmentation de la luminosité, conversion en N&B, etc).
Ceci se fait facilement avec des outils comme [Imagemagik](https://imagemagick.org/).
Pour le recadrage, un outil permettant de le faire facilement est proposé, voir la section "3 - Extension" ci-dessous.

Dans l'idéal, il faudrait avoir des photos de quelques dizaines de ko.

Le script va générer en sortie deux fichiers pdf, dans le dossier courant:

* `trombi_global.pdf`: trombinoscope global, sur plusieurs pages;
* `trombi_groupes.pdf`: trombinoscope avec une page par groupe, avec les étudiants faisant partie de ce groupe.

### 3.1 - Données d'entrées du script

* une liste en CSV contenant sur 3 champs:
Groupe, Nom, Prénom <br>
A coller dans le dossier racine. Les lignes vides seront ignorées.
* copier dans un sous-dossier `photos` les photos, dans l'ordre de la liste.

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


### 3.2 - Paramétrage
* éditer le fichier `entete_ecole.txt` et y mettre le nom de l'établissement, de la promo, etc.
Sera imprimé dans l'en-tête de gauche.
* éditer le fichier `entete_annee.txt` et y mettre l'année en cours (ou ce que vous voulez d'autre!).
Sera imprimé dans l'en-tête de droite.

### 3.3 - Syntaxe d'appel

Des valeurs par défaut sont prévues, mais on peut passer des options pour les modifier.

`$ trombino [-hs] [-l fichier_liste] [-p dossier_photos] [-o nom_pdf] [-c nb_cols]`

* `-l`: pour spécifier un autre nom du fichier csv d'entrée (liste des étudiants)
* `-p`: pour indiquer un autre dossier pour les photos
* `-o`: pour donner un autre nom au fichier pdf généré (sans extension!!)
<br>Par exemple, `-o aaa` produira les deux fichiers `aaa_global.pdf` et `aaa_groupes.pdf`
* `-c`: pour modifier le nombre de colonnes. La taille des photos est automatiquement ajustée.
* `-s`: permute nom - prénom
* `-f`: permet de spécifier le séparateur de champs du fichier "liste". C'est ',' par défaut.
On peut le changer pour des ';' avec `-f ";"`.
A noter que l'usage de l'espace (ASCII 32) est déconseillé, comme il est probable d'avoir des étudiants avec des noms composés.
* `-h`: affiche cette aide
* `-d`: active le mode "debug", ce qui imprimera le nom du fichier de la photo avec la photo
(utile en cas d'erreur nom/photo)

 
## 4 - Exemple/demo

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

## 5 - Extension optionnelle: recadrage assisté

### 5.1 - Introduction
L'un des problèmes que l'on rencontre avec cette approche est le fait qu'il nécessite en pratique un "cropping" des photos.
En effet, en général le cadrage fait qu'il est peu pratique d'avoir dès la prise de vue un cadrage type "photo d'identité".
Le cropping peut se faire à la main, photo par photo, à l'aide d'un outil ad hoc, mais c'est évidemment fastidieux (et donc, non, on oublie).
On peut aussi l'automatiser via un script (utilisant par exemple [imagemagick](https://imagemagick.org/)) qui prend chaque photo et lui applique un cropping fixe, mais il faut alors prédéterminer la bonne "bounding box", ce qui prend du temps.
Sans compter que on aura toujours des étudiants qui sont un peu trop à gauche, un peu trop à droite, et donc le cropping identique pour toutes les photos va générer soit des "coupages de têtes", soit des images avec un cadrage un peu trop "large".

Depuis 2024/09, une extension utilisant Python3 et la bibliothèque OpenCv est incluse dans ce projet et permet d'avoir un **cropping assisté**, par une détection de visage dans la photo.

### 5.2 - Outils nécessaires
Il faut donc avoir ces deux outils installé localement (Python3 est en général déjà présent).
Pour Opencv, l'installation est assez facile, via:
```
$ pip install opencv-python
```
Ceci a été testé avec la version 4.5.5, mais devrait aussi fonctionner avec des versions 3.

### 5.3 - Utilisation

L'utilisation se fait via l'appel du programme `autocrop` depuis le dossier courant.
Ce programme prend deux arguments:

- Le premier est le nom du dossier dans lequel se trouve les photos brutes.
- Le second est le nom du dossier dans lequel seront placés les images "croppées"
(sera crée s'il n'existe pas).

Par exemple:
```
$ autocrop src dst
```

Ce programm est un script bash qui lance pour chaque fichier du dossier de photos le programme Python `trombino_autocrop_gui.py`.
Ce dernier va lancer lancer une cascade de classifieurs pour tenter de trouver un visage
(voir
https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html
pour des détails), avec des valeurs de paramètres par défaut.
Si les paramètres par défaut ne trouvent pas de visage, alors une interface graphique est démarrée
(basée sur le module "HighGui" de OpenCV).
Des sliders permettent d'ajuster les paramètres, le plus important étant l'échelle ("scale").
Une fois un visage trouvé, il faut alors appuyer sur "espace" pour sauvegarder l'image "croppée".

Dans le cas où il s'agit d'une photo "vide", un appui sur ESC va sauvegarder la photo telle quelle.


