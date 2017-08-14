#!/bin/csh
#
# to be run in it0

foreach i ( `cat file.nam` )
	echo $i `grep energies $i` >> energies
end

awk '{print $1,$11}' energies | sed 's/,//g' > a
/bin/mv -f a energies
awk '{print $2}' energies > viol
