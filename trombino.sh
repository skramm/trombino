#!/bin/bash

# S. Kramm - 2022
# https://github.com/skramm/trombino
# création automatique de trombinoscope

# part 1: création du fichier contenant les paires photo - Id


# dossier par défaut contenant les photos
photos=photos/

# fichier csv d'entrée par défaut contenant groupe,nom,prénom
input_file=liste.csv

# nom fichier de sortie par défaut
outfile1=trombi

# nb de colonnes par défaut
nb_cols=4

# initialisation variables
count_lines=0
count_cols=0
count_pages=0

current_group=nogroup
header_file=trombi_header.tex


#-----------------------------------------------------------------------------
# FONCTIONS
#-----------------------------------------------------------------------------
function close_page
{
	if $table_is_closed ; then
		return;
	fi

	(( count_cols+=1 ))
	if ! $line_is_closed ;
	then
		while [ $count_cols != $nb_cols ]
		do
			echo "&" >>$outfile
			(( count_cols+=1 ))
		done
		echo "\\\ \hline" >>$outfile
	fi
	echo "\end{tabularx}" >>$outfile
	echo "" >>$outfile
	echo "\clearpage" >>$outfile
	line_is_closed=true
	table_is_closed=true;
}
function reset_all
{
	count_lines=0
	count_cols=0
}
function new_page
{
	echo "\begin{center}" >>$outfile
	echo "\bf \huge" >>$outfile
	echo "Groupe $1" >>$outfile
	echo "\end{center}" >>$outfile

	echo "" >>$outfile
	echo -n "\begin{tabularx}{\linewidth}{|" >>$outfile
	for (( i=0;i<$nb_cols;i++ ))
	do
		printf "X|" >>$outfile	
	done
	echo "}\hline" >>$outfile
	table_is_closed=false;
}

#-------------------- Main function, process one line -------------------------
function process_line
{
# args: 1: photo filename, 2: group, 3: name, 4: firstname, 5: bac
#	echo -e "\n* processing name=$4 $3 current_group=$current_group bac=$5 photo=$1"

# SI nouveau groupe, alors il faut fermer la page et faire une nouvelle
	if [ "$current_group" != "$2" ]; then
		if [ "$current_group" != "nogroup" ]; then
			close_page
		fi
		current_group=$2
		reset_all
	fi

	if [ "$count_lines" -eq "0" ] &&  [ "$count_cols" -eq "0" ]; then
		new_page $2
	fi
	line_is_closed=false

	photo="${1%.*}"
	echo "\includegraphics[width=$width\textwidth]{$photo} \newline" >>$outfile
	echo "$3 $4 $5" >>$outfile
	(( count_cols += 1 ))

	if [ "$count_cols" -eq "$nb_cols" ]; then
		echo "\\\ \hline" >>$outfile
		line_is_closed=true
		(( count_lines += 1 ))
		count_cols=0
	else
		echo "&" >>$outfile

	fi

#	echo "count_cols=$count_cols count_lines =$count_lines  count_pages=$count_pages"
}


# ----------------------------------------------------------------------------
# DEBUT SCRIPT 

# etape 1: lecture des parametres

while [ -n "$1" ]; do # while loop starts
	case "$1" in
	-l)
		input_file="$2"
		shift
		;;
	-p)
		photos="$2"
		shift
		;;
	-c)
		nb_cols="$2"
		shift
		;;
	-o)
		outfile1="$2"
		shift
		;;	
	*) echo " -Erreur: option $1 inconnue"; exit 1 ;;
	esac
	shift
done

if [ -f $input_file ]; then
	echo " -Lecture liste dans fichier '$input_file'"
else
	echo " -Erreur: fichier '$input_file' introuvable!"
	exit 2
fi	

if [ -d $photos ]; then
	echo " -Lecture des photos dans dossier '$photos'"
else
	echo " -Erreur: dossier '$photos' introuvable!"
	exit 3
fi	

echo " -Nom du fichier de sortie: ${outfile1}.pdf"
outfile=BUILD/$outfile1.tex

echo " -Nbe colonnes par page=$nb_cols"

# calcul largeur cellule en fonction du nbe de colonnes
width=$(bc <<< "scale=2;0.95/$nb_cols")
#echo "width=$width"

# liste des photos
ls $photos -1 > BUILD/list_photos.txt

# check
sed '/^[[:space:]]*$/d' $input_file > BUILD/input.csv
n1=$(wc -l <BUILD/input.csv)
n2=$(wc -l <BUILD/list_photos.txt)
if [ $n1 != $n2 ]
then
	echo " -Erreur, $n2 photos et $n1 noms dans la liste!"
	exit 1
fi
echo " -Lecture de $n1 personnes & photos"

echo "* Etape 1: génération fichiers intermédiaires"

# merge photos + noms/groupes
paste --delimiters="," BUILD/list_photos.txt BUILD/input.csv > BUILD/global_list_1.csv

# tri
sort -t, -k2,3 BUILD/global_list_1.csv >BUILD/global_list_2.csv

if [ ! -f BUILD/global_list_2.csv ]; then
	echo " -Erreur: fichier intermédiaire BUILD/global_list_2.csv absent..."
	exit 5
fi

# Génération du .tex

if [ ! -f "$header_file" ]; then
    echo " -Erreur: fichier d'en-tête introuvable"
	exit
fi

cat $header_file >$outfile
cat entete_ecole.txt >>$outfile
echo "}">>$outfile
echo "\rhead{">>$outfile
cat entete_annee.txt >>$outfile
echo "}">>$outfile
echo "\begin{document}\noindent">>$outfile
echo "\graphicspath{ {../$photos/} }">>$outfile

IFS=,
while read line; do
#     echo "line : $line"
	process_line $line
done < BUILD/global_list_2.csv

# close what might need to be closed

if [ "$count_cols" -ne "0" ]; then
	close_page
	echo
fi

if ! $table_is_closed ; then
	close_page
fi

# close file
echo "" >>$outfile
echo "\end{document}" >>$outfile

cd BUILD
echo "* Etape 2: start pdflatex"
pdflatex -interaction=batchmode $outfile1 1>pdflatex.stdout 2>pdflatex.stderr
if [ $? != 0 ]; then
	echo " -Erreur de compilation, voir fichier log"
else
	echo " -Compilation: ok"
fi

if [ -f $outfile1.pdf ]; then
	echo " -Fichier $outfile1.pdf généré"
	mv $outfile1.pdf ..
else
	echo " -Erreur fatale, pas de pdf généré"
fi
cd ..

exit 0


# ----------------------------------------------------------------------------


