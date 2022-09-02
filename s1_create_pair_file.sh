#!/bin/bash

# S. Kramm - 2016-2022
# https://github.com/skramm/trombino
# création automatique de trombinoscope

# part 1: création du fichier contenant les paires photo - Id


# dossier contenant les photos
photos=photos/

# fichier csv d'entrée par défaut contenant groupe,nom,prénom
input_file=liste.csv


# ----------------------------------------------------------------------------

if [ "$1" != "" ]; then
	input_file=$1
fi

if [ -f $input_file ]; then
	echo "Lecture liste dans fichier '$input_file'"
else
	echo "Erreur: fichier '$input_file' introuvable!"
	exit 1
fi	

# liste des photos
ls $photos -1 > BUILD/list_photos.txt

# check
n1=$(wc -l <$input_file)
n2=$(wc -l <BUILD/list_photos.txt)
if [ $n1 != $n2 ]
then
	echo "Erreur, $n2 photos et $n1 noms dans la liste!"
	exit 1
fi
echo "Lecture de $n1 personnes & photos"

# merge photos + noms/groupes
paste --delimiters="," BUILD/list_photos.txt $input_file > BUILD/global_list_1.csv

# tri
sort -t, -k2,3 BUILD/global_list_1.csv >BUILD/global_list_2.csv

# ----------------------------------------------------------------------------


