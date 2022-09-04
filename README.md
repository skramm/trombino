# Trombino
Génération de trombinoscope en pdf automatique, à partir d'une liste et d'un ensemble de photos.

* auteur: Sebastien Kramm
* statut: stabilisé en v1 (2022-09-03)
* home page: https://github.com/skramm/trombino
* licence: [WTFPL](https://en.wikipedia.org/wiki/WTFPL)

Calibré pour des groupes de 5-16 personnes par page, pour une année d'une promo de type universitaire (20-100 ou plus personnes).


## Exemple de résultat (réel)

![exemple](trombi_1_800.jpg)


## Outils nécessaires
* bash
* LaTeX, avec le package `tabularx`

## Utilisation

Il faut avoir une liste des personnes, et prendre une photo par personne, **dans l'ordre de la liste**.
En cas d'absence, il faut prendre une photo "vide", pour conserver l'ordre.

Ensuite, un petit traitement batch des photos est probablement nécessaire (recadrage, augmentation de la luminosité, conversion en N&B, etc).
Ceci se fait facilement avec des outils comme [Imagemagik](https://imagemagick.org/).
Dans l'idéal, il faudrait avoir des photos de quelques dizaines de ko.


## Données d'entrées du script
* une liste en CSV contenant sur 3 champs: Groupe, Nom, Prénom, à coller dans le dossier racine
Les lignes vides seront ignorées.
* copier dans le dossier `photos` les photos, dans l'ordre de la liste.

Attention, il doit y avoir autant de photos que de lignes dans le fichier d'entrée!

## Paramétrage
* éditer le fichier `entete_ecole.txt` et y mettre le nom de l'établissement, de la promo, etc.
Sera imprimé dans l'en-tête de gauche.
* éditer le fichier `entete_annee.txt` et y mettre l'année en cours (ou ce que vous voulez d'autre!).
Sera imprimé dans l'en-tête de droite.

## Syntaxe d'appel

Des valeurs par défaut sont prévues, mais on peut passer des options pour les modifier.

`$ ./trombino.sh [-l fichier_liste] [-p dossier_photos] [-o nom_pdf] [-c nb_cols]`

* `-l`: pour spécifier un autre nom du fichier "liste"
* `-p`: pour indiquer un autre dossier pour les photos
* `-o`: pour donner un autre nom au fichier pdf généré (sans extension!!)
* `-c`: pour  modifier le nombre de colonnes
 
Attention, si trop de colonnes, on aura une erreur de compilation LaTeX, mais le fichier de sortie devrait être généré quand même.

## Exemple/demo

Des données de démo dont incluses, vous pouvez tester directement.
Il y a:

* une liste de noms (thx: https://fossbytes.com/tools/random-name-generator)
* une liste de "photos" (thx: https://multiavatar.com/)
Ces avatars sont générés via le script `gen_avatars.sh` (requires Imagemagick)

Tapez la commande suivante dans le dossier racine, une fois le repo cloné:
```
$ ./trombino.sh
```
Ceci doit vous donner dans un fichier `trombi.pdf`, similaire à celui qui est fourni (`trombi_exemple.pdf`).


