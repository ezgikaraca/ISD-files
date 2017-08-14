#!/bin/csh
# csh script to prepare selected structures for it1
mkdir file_reserve
mv file.* file_reserve
sed 'h;:a;s/[^\n]\+/&/10;t;G;ba' viol.sele > file.nam
touch file.list
foreach i (`cat file.nam`)
	grep $i file_reserve/file.list >> file.list
end
awk '{print FNR}' file.nam > number
head -8 file_reserve/file.cns > file.cns
paste number file.list | awk '{printf "evaluate (&filenames.bestfile_%s=%s)\n", $1,$2}' >> file.cns
rm -rf number
