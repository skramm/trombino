# trombino
Génération de trombinoscope automatique,

* auteur: Sebastien Kramm
* statut: quasi-pret ! (2022-09-02)
* home page: https://github.com/skramm/trombino
* licence: [WTFPL](https://en.wikipedia.org/wiki/WTFPL)

Calibré pour des groupes de 5-16 personnes par page, pour une année d'une promo de type universitaire (20-100 ou plus personnes).


## Exemple de résultat

![exemple](trombi_1_800.jpg)


## Outils nécessaires
* bash
* LaTeX, avec le package `tabularx`

## Utilisation

Il faut avoir une liste des personnes, et prendre une photo par personne, **dans l'ordre de la liste**.
En cas d'absence, il faut prendre une photo "vide", pour conserver l'ordre.

Ensuite, un petit traitement batch des photos peut être pertinent (recadrage, augmentation de la luminosité, conversion en N&B, etc).
Ceci se fait facilement avec des outils comme [Imagemagik](https://imagemagick.org/).


## Données d'entrées
* une liste en CSV contenant sur 3 champs: Groupe, Nom, Prénom, à coller dans le dossier racine, avec le nom `liste.csv`
* copier dans le dossier `photos` les photos, dans l'ordre de la liste.

## Paramétrage
* éditer le fichier `trombi_header.tex` pour y mettre le nom de l'établissement, l'année, etc.

## Fonctionnement

Syntaxe:

On peut changer le nom du fichier d'entrée et/ou le dossier où se trouve les photos et/ou le nom du fichier pdf généré.

Attention, il doit y avoir autant de photos que de lignes dans le fichier d'entrée!

`$ ./trombino.sh [-l fichier_liste] [-p dossier_photos] [-o nom_pdf] [-c nb_cols]`

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



