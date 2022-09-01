#!/bin/bash

# S. Kramm 
# création automatique de trombinoscope
# part 1: création du fichier contenant les paires photo - Id


# dossier contenant les photos
photos=photos/

# fichier csv d'entrée contenant  groupe,nom,prénom
input_file=liste_RT1_20220901.csv


# ----------------------------------------------------------------------------

# liste des photos
ls $photos -1 > BUILD/list_photos.txt

# check
n1=$(wc -l <$input_file)
n2=$(wc -l <BUILD/list_photos.txt)
if [ $n1 != $n2 ]
then
	echo "Erreur, $n1 photos et $n2 noms dans la liste!"
	exit 1
fi
echo "Lecture de $n1 personnes"

# merge photos + noms/groupes
paste --delimiters="," BUILD/list_photos.txt $input_file > BUILD/global_list_1.csv

# tri
sort -t, -k2,3 BUILD/global_list_1.csv >BUILD/global_list_2.csv

# ----------------------------------------------------------------------------


