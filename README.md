# trombino
Génération de trombinoscope automatique,

Calibré pour des groupes de 5-16 personnes par page, pour une année d'une promo de type universitaire (20-100 ou plus personnes).

* statut: quasi-pret ! (2022-09-02)
* home: https://github.com/skramm/trombino

## Exemple de résultat

![exemple](trombi_1_800.jpg)


## Outils nécessaires
* bash
* LaTeX

## Utilisation

Il faut avoir une liste des personnes, et prendre une photo par personne, **dans l'ordre de la liste**. Ensuite, un petit traitement batch des photos peut être pertinent (recadrage, augmentation de la luminosité, conversion en N&B, etc).

Tout ceci se fait facilement avec des outils comme [Imagemagik](https://imagemagick.org/).


## Données d'entrées
* une liste en CSV contenant sur 3 champs: Groupe, Nom, Prénom, à coller dans le dossier racine, avec le nom `liste.csv`
* copier dans le dossier `photos` les photos, dans l'ordre de la liste.

## Paramétrage
* éditer le fichier `trombi_header.tex` pour y mettre le nom de l'établissement, l'année, etc.
* éditer le fichier `s2_create_trombi.sh` pour modifier le nom du fichier de sortie
* si besoin de modifier le nb de colonnes, c'est également dans ce fichier que ça se passe.

## Fonctionnement

Le programme est découpé en 2 scripts bash, qu'il faut appeler successivement.

* `s1_create_pair_file.sh`: va générer un fichier contenant l'association photo-nom, qui va servir d'entrée au 2è programme.
Par défaut, il utilise comme fichier d'entrée `liste.csv` mais on peut passer un autre nom de fichier en argument.
* `s2_create_trombi.sh`: va générer le fichier LaTeX (stocké dans `BUILD`), et appelle le compilateur `pdflatex` pour générer le pdf.
Le nom du fichier pdf généré est par défaut `trombi.pdf` mais on peut passer un autre nom en argument (sans l'extension!).

## Exemple/demo

Des données de démo dont incluses, vous pouvez tester directement.
Il y a

* une liste de noms (thx: https://fossbytes.com/tools/random-name-generator)
* une liste de "photos" (thx: https://multiavatar.com/)
Ces avatars sont générés via le script `gen_avatars.sh`



