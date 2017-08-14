#!/bin/csh
# change segid and reference pdb, i.e. protein1_aligned.pdb for every calculation

set id = protein1 # to be modified
set segid = A # to be modified

foreach i(*fit)
	set m = `echo $i | sed 's/\.fit//g'`
	cp "$m".fit model.pdb
	touch "$m"_cns.out
	cns << _Eod_ >> "$m"_cns.out
  	   struc @../complex.psf end
  	   do (mass=1) (all)
  	   coor @model.pdb
  	   coordinates disposition=comparison @../"$id"_aligned.pdb
  	   coor fit sele=(segid $segid) LSQ=FALSE end
  	   coor fit sele=(segid $segid) end
  	   stop
_Eod_
end
/bin/rm -f model.pdb *fit

touch trans
touch rot
foreach m(`cat file.nam`)
  set i = `echo $m | sed 's/\.fit/_cns\.out/g'`
  grep Translation $i | head -1 | sed 's/(//g' | sed 's/)//g' | awk '{print $5,$6,$7}' >> trans
  grep "Corresp. rotation angle" $i | awk '{print $4,$7,$8,$9}' >> rot
end

paste trans rot > trans_rot.dat

awk '{print $1,$2,$3,$4,$5,$6,$7}' trans_rot.dat > a
/bin/mv -f a trans_rot.dat
/bin/rm -f trans rot
mv trans_rot.dat trans_rot.dat_"$id"
