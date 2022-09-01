# trombino
Génération de trombinoscope

## Outils nécessaires
* bash
* LaTeX

## Données d'entrées
* une liste en CSV contenant sur 3 champs: groupe, Nom, Prénom
* un dossier contenant les photos, dans l'ordre de la liste


## Fonctionnement

Le programme est découpé en 2 scripts bash, qu'il faut appeler successivement.
* `s1_create_pair_file.sh`: va générer un fichier contenant l'association photo-nom, qui va servir d'entrée au 2è programme.
* `s2_create_trombi.sh`: va générer le fichier LaTeX, et appelle le compilateur `pdflatex` pour générer le pdf.

