#!/bin/bash

# S. Kramm - sept 2016 - 2022
# https://github.com/skramm/trombino
# création automatique de trombinoscope

# part 2: génération du fichier source Latex et compilation en pdf

# le fichier d'entrée doit être trié par groupe


#nb_lines=4
nb_cols=4

count_lines=0
count_cols=0
count_pages=0

current_group=nogroup
outfile=BUILD/trombi_PROMO_ANNEE.tex
photos=photos/

header_file=trombi_header.tex
input_file=BUILD/global_list_2.csv

#------------------------------------------------------------------------------------------------
function close_page
{
	if $table_is_closed ; then
		return;
	fi
	echo "func: close_page"
	if ! $line_is_closed ;
	then
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
	echo "\begin{tabularx}{\linewidth}{|X|X|X|X|}" >>$outfile
	echo "\hline" >>$outfile
	table_is_closed=false;
}
#------------------------------ Main function, process one line ----------------------------------

function process_line
{
# args: 1: photo filename, 2: group, 3: name, 4: firstname, 5: bac
	echo -e "\n* processing name=$4 $3 current_group=$current_group bac=$5 photo=$1"

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
	echo "photo=$photo"
	echo "\includegraphics[width=36mm]{$photo} \newline" >>$outfile
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

	echo "count_cols=$count_cols count_lines =$count_lines  count_pages=$count_pages"
}



# ----------------------------------------------------------------------------

# DEBUT SCRIPT

if [ ! -f "$header_file" ]; then
    echo "Error: header file not found, exiting..."
	exit
fi

cat $header_file >$outfile
echo "\graphicspath{ {$photos} }">>$outfile


IFS=,
while read line; do
     echo "line : $line"
	process_line $line
done < $input_file

# close what might need to be closed

if [ "$count_cols" -ne "0" ]; then
	echo "\\\ \hline" >>$outfile;
	close_page
	echo
fi

if ! $table_is_closed ; then
	close_page
fi

# close file
echo "" >>$outfile
echo "\end{document}" >>$outfile

#set -x
#cd BUILD
echo "start pdflatex"
pdflatex -interaction=batchmode $outfile 1>BUILD/pdflatex.stdout 2>BUILD/spdflatex.stderr
#cd ..


# ----------------------------------------------------------------------------


