# trombino
Génération de trombinoscope.

Calibré pour des groupes de 5-16 personnes par page.

![exemple](trombi_1_800.jpg)


## Outils nécessaires
* bash
* LaTeX

## Données d'entrées
* une liste en CSV contenant sur 3 champs: Groupe, Nom, Prénom, à coller dans le dossier racine, avec le nom `liste.csv`
* copier dans le dossier `photos` les photos, dans l'ordre de la liste.

## Paramétrage
* éditer le fichier `header.tex` pour y mettre le nom de l'établissement, l'année, etc.
* 

## Fonctionnement

Le programme est découpé en 2 scripts bash, qu'il faut appeler successivement.
* `s1_create_pair_file.sh`: va générer un fichier contenant l'association photo-nom, qui va servir d'entrée au 2è programme.
* `s2_create_trombi.sh`: va générer le fichier LaTeX, et appelle le compilateur `pdflatex` pour générer le pdf.

