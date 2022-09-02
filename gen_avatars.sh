n=35
for (( i=0; i<n;i++ ))
do
	echo $i
	wget https://api.multiavatar.com/$i.png
	convert $i.png photos/p$i.jpg
	rm $i.png
done

